"""Self-checks for sample_op.py: true negatives on clean output, and seeded
faults on disposable copies that the checks must catch.

    python -m pytest tests/test_sample_op.py   (or: python -m unittest discover tests)
"""
import json, os, subprocess, sys, tempfile, unittest
import numpy as np

TOOLS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools")
sys.path.insert(0, TOOLS)
import sample_op as so  # noqa: E402
# Optional real-material check. The V1 original used a third-party library
# sample that is not redistributed here; point this at any sustained stereo
# PCM WAV to run it.
VOCREV = os.environ.get("SAMPLE_OP_REAL_MATERIAL", "")
SR = 44100


def jload(path):
    with open(path) as f:
        return json.load(f)

def cli(*args):
    r = subprocess.run([sys.executable, os.path.join(TOOLS, "sample_op.py"), *map(str, args)], capture_output=True, text=True)
    return r.returncode, (json.loads(r.stdout.strip().splitlines()[-1]) if r.stdout.strip() else r.stderr)

def failed(manifest_path):
    m = jload(manifest_path)
    return sorted({c["name"] for c in m["checks"] if c["required"] and not c["passed"]})

def sustained(seconds=2.0, ch=2, amp=0.5):
    """Tone + noise with no silent regions, so any cut lands on signal."""
    t = np.arange(int(seconds * SR)) / SR
    rng = np.random.RandomState(7)
    base = amp * (0.7 * np.sin(2 * np.pi * 220 * t) + 0.3 * np.sin(2 * np.pi * 331 * t + 1))
    x = np.stack([base + 0.001 * rng.randn(len(t)) for _ in range(ch)], axis=1)
    return x


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="sample_op_test_")
        self.d = self._tmp.name
        self.src = os.path.join(self.d, "src.wav")
        so.write_wav(self.src, sustained(), SR, 16)

    def tearDown(self):
        self._tmp.cleanup()

    def p(self, name):
        return os.path.join(self.d, name)


class Slice(Base):
    def test_control_path_reconstructs_exactly(self):
        code, out = cli("slice", self.src, "--cuts", "0.1s,4725,0.5s,777ms,1.9s", "--fade", "none",
                        "--out-dir", self.d, "--prefix", "ctl")
        self.assertEqual(code, 0, out)
        m = jload(self.p("ctl.manifest.json"))
        rec = [c for c in m["checks"] if c["name"] == "reconstruction_null"][0]
        self.assertTrue(rec["passed"] and rec["required"] and rec["max_abs_diff"] == 0.0)
        # the raw cuts on sustained material ARE clicks: reported, not required under --fade none
        clicks = [c for c in m["checks"] if c["name"] == "boundaries_click_free"]
        self.assertTrue(all(not c["required"] for c in clicks))
        self.assertTrue(any(not c["passed"] for c in clicks))

    def test_faded_slices_are_click_free_and_untouched_inside(self):
        code, out = cli("slice", self.src, "--cuts", "0.1s,0.2s,0.35s,0.5s", "--out-dir", self.d, "--prefix", "cs")
        self.assertEqual(code, 0, out)
        m = jload(self.p("cs.manifest.json"))
        for o in m["outputs"]:
            self.assertEqual((o["sample_rate"], o["channels"]), (SR, 2))
            self.assertEqual(o["fade_in_samples"], round(so.DEFAULT_FADE_MS * SR / 1000))
        self.assertTrue(all(c["passed"] for c in m["checks"] if c["name"] in ("boundaries_click_free", "unfaded_region_exact")))

    def test_auto_fade_leaves_quiet_edges_alone(self):
        x = sustained(1.0); x[:2000] = 0                     # attack from silence: must not be faded
        so.write_wav(self.p("gated.wav"), x, SR, 24)
        code, _ = cli("slice", self.p("gated.wav"), "--ranges", "0-0.5s", "--out-dir", self.d, "--prefix", "g")
        self.assertEqual(code, 0)
        o = jload(self.p("g.manifest.json"))["outputs"][0]
        self.assertEqual((o["fade_in_samples"], o["fade_out_samples"]), (0, round(so.DEFAULT_FADE_MS * SR / 1000)))

    def test_mono_preserved(self):
        so.write_wav(self.p("mono.wav"), sustained(0.5, ch=1), SR, 16)
        code, _ = cli("slice", self.p("mono.wav"), "--ranges", "100-0.2s", "--out-dir", self.d, "--prefix", "m")
        self.assertEqual(code, 0)
        self.assertEqual(jload(self.p("m.manifest.json"))["outputs"][0]["channels"], 1)

    def test_seeded_fault_abrupt_cut_is_detected(self):
        x, _, _ = so.load(self.src)
        s = 13000 + int(np.argmax(np.abs(x[13000:13200, 0])))  # cut on a loud phase, not a zero crossing
        e = 17000 + int(np.argmax(np.abs(x[17000:17200, 0])))
        bad = x[s:e]                                         # hard cut in sustained signal
        chk = so.boundary_check(bad, SR, [0, len(bad)])
        self.assertFalse(chk["passed"])
        self.assertEqual({c["position"] for c in chk["clicks"]}, {0, len(bad)})
        good, _, _ = so.apply_fades(bad, round(3 * SR / 1000), "auto")
        self.assertTrue(so.boundary_check(good, SR, [0, len(good)])["passed"])

    def test_seeded_fault_wrong_slice_boundary_breaks_reconstruction(self):
        x, _, _ = so.load(self.src)
        a, b, c = 4410, 9000, 20000
        off_by_one = [x[a:b], x[b + 1:c]]                    # one sample dropped at the boundary
        chk = so.null_check("reconstruction_null", np.vstack(off_by_one), x[a:c])
        self.assertFalse(chk["passed"])
        swapped = [x[b:c], x[a:b]]                           # right length, wrong order
        self.assertFalse(so.null_check("reconstruction_null", np.vstack(swapped), x[a:c])["passed"])
        shifted = [x[a:b], x[b - 1:c - 1]]                   # right length, one-sample duplicated/lost
        self.assertFalse(so.null_check("reconstruction_null", np.vstack(shifted), x[a:c])["passed"])
        self.assertTrue(so.null_check("reconstruction_null", np.vstack([x[a:b], x[b:c]]), x[a:c])["passed"])

    @unittest.skipUnless(VOCREV and os.path.exists(VOCREV), "set SAMPLE_OP_REAL_MATERIAL to a sustained PCM WAV")
    def test_real_material_hard_cut_detected_faded_passes(self):
        code, _ = cli("slice", VOCREV, "--cuts", "2s,2.1s,2.3s", "--fade", "none", "--out-dir", self.d, "--prefix", "vr_raw")
        m = jload(self.p("vr_raw.manifest.json"))
        self.assertEqual(code, 0)                            # control path: exact reconstruction is the requirement
        self.assertTrue(all(not c["passed"] for c in m["checks"] if c["name"] == "boundaries_click_free"))
        code, _ = cli("slice", VOCREV, "--cuts", "2s,2.1s,2.3s", "--out-dir", self.d, "--prefix", "vr")
        self.assertEqual(code, 0)


class Reverse(Base):
    def test_reverse_nulls_exactly(self):
        code, out = cli("reverse", self.src, "--out", self.p("rev.wav"), "--fade", "none")
        self.assertEqual(code, 0, out)
        x, _, _ = so.load(self.src); z, _, _ = so.load(self.p("rev.wav"))
        self.assertTrue(np.array_equal(z[0], x[-1]) and np.array_equal(z[-1], x[0]))
        self.assertTrue(np.array_equal(z[::-1], x))

    def test_reverse_twice_is_identity(self):
        cli("reverse", self.src, "--out", self.p("r1.wav"), "--fade", "none")
        cli("reverse", self.p("r1.wav"), "--out", self.p("r2.wav"), "--fade", "none")
        self.assertTrue(np.array_equal(so.load(self.p("r2.wav"))[0], so.load(self.src)[0]))

    def test_reverse_with_fades_keeps_interior_exact(self):
        code, _ = cli("reverse", self.src, "--out", self.p("rf.wav"), "--fade", "always", "--fade-ms", "10")
        self.assertEqual(code, 0)
        c = [c for c in jload(self.p("rf.manifest.json"))["checks"] if c["name"] == "reverse_null_unfaded_region"][0]
        self.assertTrue(c["passed"] and c["samples"] == len(so.load(self.src)[0]) - 2 * 441)

    def test_seeded_fault_one_altered_sample_fails_null(self):
        cli("reverse", self.src, "--out", self.p("rev.wav"), "--fade", "none")
        x, _, _ = so.load(self.src); z, _, _ = so.load(self.p("rev.wav"))
        z[12345, 1] += 1 / 2 ** 23                           # one LSB in one channel
        self.assertFalse(so.null_check("reverse_null", z, x[::-1])["passed"])


class Repitch(Base):
    def test_lengths_and_duration_reported(self):
        for semis in (-12, -5, 0, 3, 7, 12, 0.5):
            out = self.p(f"rp{semis}.wav")
            code, res = cli("repitch", self.src, "--semitones", semis, "--out", out)
            self.assertEqual(code, 0, (semis, res))
            m = jload(so.manifest_for(out))
            n_src, n_out = m["sources"][0]["frames"], m["outputs"][0]["frames"]
            self.assertLessEqual(abs(n_out - n_src * 2 ** (-semis / 12)), 1 + n_src * 3e-5)
            self.assertAlmostEqual(m["outputs"][0]["duration"]["duration_ratio"], n_out / n_src, places=5)

    def test_pitch_moves_in_requested_direction(self):
        t = np.arange(SR) / SR
        so.write_wav(self.p("sine.wav"), 0.5 * np.sin(2 * np.pi * 441 * t)[:, None], SR, 24)
        cli("repitch", self.p("sine.wav"), "--semitones", 12, "--out", self.p("up.wav"))
        z, _, _ = so.load(self.p("up.wav"))
        f = np.fft.rfftfreq(len(z), 1 / SR)[np.argmax(np.abs(np.fft.rfft(z[:, 0] * np.hanning(len(z)))))]
        self.assertAlmostEqual(f, 882, delta=2)

    def test_undertow_denominator_reported_as_out_of_tolerance(self):
        code, _ = cli("repitch", self.src, "--semitones", 7, "--max-denominator", 160, "--out", self.p("u7.wav"))
        self.assertEqual(code, 1)                            # 2/3 is 1.955 cents flat of equal temperament
        self.assertEqual(failed(self.p("u7.manifest.json")), ["ratio_within_cents"])

    def test_seeded_fault_truncated_output_fails_length(self):
        fr = so.ratio_for(-5)
        n = 88200; expect = -(-n * fr.numerator // fr.denominator)
        self.assertTrue(all(c["passed"] for c in so.repitch_length_check(n, expect, -5, fr, 0.05)))
        self.assertFalse(so.repitch_length_check(n, expect - 1, -5, fr, 0.05)[0]["passed"])

    def test_seeded_fault_overshoot_clipping_detected(self):
        t = np.arange(SR // 2)
        sq = np.where((t // 100) % 2 == 0, 0.999, -0.999)[:, None]    # full-scale square: resampling overshoots
        so.write_wav(self.p("sq.wav"), sq, SR, 24)
        code, _ = cli("repitch", self.p("sq.wav"), "--semitones", -3, "--out", self.p("sq_rp.wav"))
        self.assertEqual(code, 1)
        self.assertIn("no_clipping", failed(self.p("sq_rp.manifest.json")))
        code, _ = cli("repitch", self.p("sq.wav"), "--semitones", -3, "--out", self.p("sq_ok.wav"), "--allow-clip")
        self.assertEqual(code, 0)


class Arrange(Base):
    def test_arrange_places_items_exactly_with_gaps(self):
        cli("slice", self.src, "--cuts", "0.1s,0.2s,0.3s,0.4s", "--out-dir", self.d, "--prefix", "s")
        items = [self.p("s_02.wav"), "gap:4725", self.p("s_00.wav"), "gap:10ms", self.p("s_01.wav"), self.p("s_00.wav")]
        with open(self.p("items.txt"), "w") as f:
            f.write("\n".join(items))
        code, out = cli("arrange", "--out", self.p("arr.wav"), f"@{self.p('items.txt')}")
        self.assertEqual(code, 0, out)
        m = jload(self.p("arr.manifest.json"))
        lay = m["outputs"][0]["layout"]
        self.assertEqual([l["offset"] for l in lay], [0, 4410, 9135, 13545, 13986, 18396])
        self.assertEqual(m["outputs"][0]["frames"], 18396 + 4410)
        self.assertEqual(len(m["sources"]), 3)

    def test_seeded_fault_spike_at_junction_detected(self):
        cli("slice", self.src, "--cuts", "0.1s,0.2s,0.3s", "--out-dir", self.d, "--prefix", "s")
        cli("arrange", "--out", self.p("arr.wav"), self.p("s_01.wav"), self.p("s_00.wav"))
        z, _, _ = so.load(self.p("arr.wav"))
        j = 4410
        self.assertTrue(so.boundary_check(z, SR, [0, j, len(z)])["passed"])
        z2 = z.copy(); z2[j, 0] = 0.3                       # disposable copy with a one-sample spike
        chk = so.boundary_check(z2, SR, [0, j, len(z2)])
        self.assertFalse(chk["passed"])
        self.assertEqual([c["position"] for c in chk["clicks"]], [j])

    def test_unfaded_hard_items_fail_arrange_boundary_check(self):
        cli("slice", self.src, "--cuts", "0.1s,0.2s,0.3s", "--fade", "none", "--out-dir", self.d, "--prefix", "h")
        code, _ = cli("arrange", "--out", self.p("bad.wav"), "--fade", "none", self.p("h_01.wav"), "gap:50ms", self.p("h_00.wav"))
        self.assertEqual(code, 0)                            # --fade none: boundaries reported, not required
        chk = [c for c in jload(self.p("bad.manifest.json"))["checks"] if c["name"] == "boundaries_click_free"][0]
        self.assertFalse(chk["passed"])
        code, _ = cli("arrange", "--out", self.p("fixed.wav"), self.p("h_01.wav"), "gap:50ms", self.p("h_00.wav"))
        self.assertEqual(code, 0)

    def test_mismatched_format_rejected(self):
        so.write_wav(self.p("mono.wav"), sustained(0.2, ch=1), SR, 16)
        code, _ = cli("arrange", "--out", self.p("x.wav"), self.src, self.p("mono.wav"))
        self.assertNotEqual(code, 0)


class GeneralAndManifest(Base):
    def test_seeded_fault_nonfinite_detected_and_not_written(self):
        y = sustained(0.1); y[100, 0] = np.nan
        o, checks = so.emit(self.p("nan.wav"), y, SR, 24, False)
        self.assertFalse(checks[0]["passed"])
        self.assertFalse(os.path.exists(self.p("nan.wav")) or o["written"])

    def test_seeded_fault_tampered_artifact_fails_verify(self):
        cli("reverse", self.src, "--out", self.p("rev.wav"))
        code, _ = cli("verify", self.p("rev.manifest.json"))
        self.assertEqual(code, 0)
        z, _, _ = so.load(self.p("rev.wav")); z[500] *= 0.5
        so.write_wav(self.p("rev.wav"), z, SR, 24)
        code, res = cli("verify", self.p("rev.manifest.json"))
        self.assertEqual(code, 1)
        self.assertEqual(res["failed"][0]["name"], "output_matches_manifest")

    def test_seeded_fault_truncated_wav_fails_readback(self):
        y = sustained(0.1)
        so.write_wav(self.p("t.wav"), y, SR, 24)
        with open(self.p("t.wav"), "r+b") as f:
            f.truncate(os.path.getsize(self.p("t.wav")) - 30)
        checks, _ = so.readback_checks(self.p("t.wav"), y, SR, 24)
        self.assertFalse(all(c["passed"] for c in checks))

    def test_manifest_records_required_fields(self):
        cli("repitch", self.src, "--semitones", -2, "--out", self.p("r.wav"))
        m = jload(self.p("r.manifest.json"))
        for k in ("operation", "params", "sources", "outputs", "checks", "passed"):
            self.assertIn(k, m)
        for e in (m["sources"][0], m["outputs"][0]):
            for k in ("path", "sha256", "frames", "sample_rate", "channels"):
                self.assertIn(k, e)
        self.assertEqual(m["sources"][0]["sha256"], so.sha256(self.src))
        self.assertEqual(m["outputs"][0]["sha256"], so.sha256(self.p("r.wav")))

    def test_deterministic_outputs(self):
        cli("repitch", self.src, "--semitones", 5, "--out", self.p("a.wav"))
        cli("repitch", self.src, "--semitones", 5, "--out", self.p("b.wav"))
        self.assertEqual(so.sha256(self.p("a.wav")), so.sha256(self.p("b.wav")))


if __name__ == "__main__":
    unittest.main()
