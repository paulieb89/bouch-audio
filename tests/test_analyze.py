"""Tests for tools/analyze.py's whole-file, --sections and --window modes.

Run with: python -m pytest tests/test_analyze.py -v   (needs numpy, scipy, pytest)
"""
import os
import sys
import wave

import numpy as np
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import analyze  # noqa: E402


def write_wav_24bit(path, samples, fs):
    """samples: float64 array, shape (n, channels), range [-1, 1]."""
    _, ch = samples.shape
    ints = np.clip(np.round(samples * 8388607.0), -8388608, 8388607).astype(np.int32)
    raw = bytearray()
    for frame in ints:
        for v in frame:
            raw += int(v).to_bytes(3, byteorder="little", signed=True)
    w = wave.open(path, "wb")
    w.setnchannels(ch)
    w.setsampwidth(3)
    w.setframerate(fs)
    w.writeframes(bytes(raw))
    w.close()


@pytest.fixture(scope="module")
def tone_24bit(tmp_path_factory):
    """2.0s, 44.1kHz, stereo, 24-bit, a pure 440Hz tone at -6.02dBFS on both
    channels — a known signal whose spectral centroid and peak are
    predictable, so this is a real regression check, not just "whatever the
    code currently outputs"."""
    fs = 44100
    dur = 2.0
    t = np.arange(int(fs * dur)) / fs
    tone = 0.5 * np.sin(2 * np.pi * 440.0 * t)
    stereo = np.stack([tone, tone], axis=1)
    path = str(tmp_path_factory.mktemp("audio") / "tone.wav")
    write_wav_24bit(path, stereo, fs)
    return path


# ---------------------------------------------------------------- 24-bit decode

def test_read_wav_24bit_roundtrip(tmp_path):
    """Directly pins read_wav's 24-bit decode against known int24 values —
    the exact thing the ad hoc script in designed-sound-palette-01 got wrong
    on its first attempt."""
    fs = 44100
    path = str(tmp_path / "known.wav")
    raw = bytearray()
    for v in (0, 8388607, -8388608, -1, 4194304):  # 0, max, min, -1, +0.5 FS
        raw += int(v).to_bytes(3, byteorder="little", signed=True) * 2  # both channels
    w = wave.open(path, "wb")
    w.setnchannels(2)
    w.setsampwidth(3)
    w.setframerate(fs)
    w.writeframes(bytes(raw))
    w.close()

    x, sr = analyze.read_wav(path)
    assert sr == fs
    assert x.shape == (5, 2)
    np.testing.assert_allclose(x[0], [0.0, 0.0], atol=1e-9)
    np.testing.assert_allclose(x[1], [1.0, 1.0], atol=1e-7)
    np.testing.assert_allclose(x[2], [-1.0, -1.0], atol=1e-7)
    np.testing.assert_allclose(x[3], [-1.0 / 8388608, -1.0 / 8388608], atol=1e-9)
    np.testing.assert_allclose(x[4], [0.5, 0.5], atol=1e-7)


# ---------------------------------------------------------------- whole-file regression

def test_whole_file_mode_on_known_tone(tone_24bit):
    """Regression fixture: a known 440Hz/-6dBFS/24-bit tone must keep
    producing the metrics that signal implies. If a future edit to
    compute_report() breaks whole-file behaviour, this fails."""
    report = analyze.analyze(tone_24bit)

    assert report["channels"] == 2
    assert report["sample_rate"] == 44100
    assert report["duration_s"] == pytest.approx(2.0, abs=0.01)
    assert report["clipped_samples"] == 0
    assert report["sample_peak_dbfs"] == pytest.approx(-6.02, abs=0.05)
    assert report["true_peak_dbtp"] == pytest.approx(-6.02, abs=0.2)
    # identical L/R -> perfectly correlated, no side energy
    assert report["stereo_correlation"] == pytest.approx(1.0, abs=0.01)
    # a pure 440Hz tone's PSD is centred on 440Hz
    assert report["spectral_centroid_hz"] == pytest.approx(440.0, rel=0.05)
    assert report["band_energy_pct"]["mid_400_2k"] > 95.0
    # 2s of continuous tone is enough for BS.1770 gating to produce a number
    assert report["lufs_integrated"] is not None
    assert "window_s" not in report
    assert "sections" not in report


def test_sections_mode_unchanged(tone_24bit):
    report = analyze.analyze(tone_24bit, sections=[["first_second", 0.0, 1.0]])
    assert len(report["sections"]) == 1
    assert report["sections"][0]["name"] == "first_second"
    assert report["sections"][0]["peak_dbfs"] == pytest.approx(-6.02, abs=0.1)


# ---------------------------------------------------------------- window mode

def test_window_mode_same_metric_shape_minus_time_gated_fields(tone_24bit):
    report = analyze.analyze(tone_24bit, window=(0.5, 0.05))

    assert report["window_s"] == [0.5, 0.55]
    assert report["channels"] == 2
    assert report["sample_rate"] == 44100
    assert report["duration_s"] == pytest.approx(0.05, abs=0.001)
    # a pure tone's centroid is still meaningful in a short window
    assert report["spectral_centroid_hz"] == pytest.approx(440.0, rel=0.15)
    assert report["true_peak_dbtp"] is not None
    assert report["sample_peak_dbfs"] is not None
    # 50ms < BS.1770's 400ms gating block and < LRA's 3s short-term block:
    # these must come back null, not a misleading number
    assert report["lufs_integrated"] is None
    assert report["lra_lu"] is None


def test_window_mode_on_24bit_wav_does_not_crash(tone_24bit):
    """The whole point of this feature: it must work on a 24-bit render
    without a bespoke decode, unlike the ad hoc script it replaces."""
    _, fs = analyze.read_wav(tone_24bit)
    assert fs == 44100
    report = analyze.analyze(tone_24bit, window=(0.0, 0.02))
    assert report["window_s"] == [0.0, 0.02]


@pytest.mark.parametrize("window", [
    (-0.1, 0.05),   # negative start
    (1.99, 0.5),    # runs past end of file
    (0.5, 0.0),     # zero duration
    (0.5, -0.01),   # negative duration
])
def test_window_bounds_are_validated(tone_24bit, window):
    with pytest.raises(ValueError):
        analyze.analyze(tone_24bit, window=window)


def test_sections_and_window_are_mutually_exclusive_at_cli_level(tone_24bit):
    argv = ["analyze.py", tone_24bit, "--sections", "/dev/null", "--window", "0.0", "0.05"]
    old = sys.argv
    sys.argv = argv
    try:
        with pytest.raises(SystemExit) as e:
            analyze.main()
        assert e.value.code == 2
    finally:
        sys.argv = old


# ---------------------------------------------------------------- transient example

def _fm_bell(fs, dur, index_peak):
    """Carrier 440 Hz, modulator ratio 3.35, modulation index decaying fast —
    the same 2-operator shape as the V2 Dexed bell. index_peak=0 is the
    modulator-off control."""
    t = np.arange(int(fs * dur)) / fs
    index = index_peak * np.exp(-t / 0.03)
    y = 0.5 * np.sin(2 * np.pi * 440 * t + index * np.sin(2 * np.pi * 440 * 3.35 * t)) * np.exp(-t / 1.5)
    return np.stack([y, y], axis=1)


def test_window_mode_sees_an_attack_transient_whole_file_misses(tmp_path):
    """Synthetic reproduction of the finding that justified --window
    (V2 designed-sound-palette-01): a decaying FM modulator barely moves the
    whole-file centroid but is plain in a 21 ms attack window. The off/on pair
    is the seeded negative/positive."""
    fs = 44100
    off, on = str(tmp_path / "off.wav"), str(tmp_path / "on.wav")
    write_wav_24bit(off, _fm_bell(fs, 4.0, 0.0), fs)
    write_wav_24bit(on, _fm_bell(fs, 4.0, 6.0), fs)
    whole_off, whole_on = analyze.analyze(off), analyze.analyze(on)
    assert whole_on["spectral_centroid_hz"] == pytest.approx(whole_off["spectral_centroid_hz"], rel=0.1)
    attack_off = analyze.analyze(off, window=(0.0, 0.02114))
    attack_on = analyze.analyze(on, window=(0.0, 0.02114))
    assert attack_on["spectral_centroid_hz"] > attack_off["spectral_centroid_hz"] + 200


# The original real-render regression, runnable where the V2 renders exist
# (they are gitignored there and not redistributed here):
#   ANALYZE_BELL_RENDERS=<dir with bell_test_op2off.wav and bell_test_algo5.wav>
_BELL_DIR = os.environ.get("ANALYZE_BELL_RENDERS", "")
BELL_OP2OFF = os.path.join(_BELL_DIR, "bell_test_op2off.wav")
BELL_ALGO5 = os.path.join(_BELL_DIR, "bell_test_algo5.wav")


@pytest.mark.skipif(
    not (_BELL_DIR and os.path.exists(BELL_OP2OFF) and os.path.exists(BELL_ALGO5)),
    reason="set ANALYZE_BELL_RENDERS to the V2 designed-sound-palette-01 render directory",
)
def test_window_mode_reproduces_the_fm_falsification_result():
    """The actual renders from V2 designed-sound-palette-01: whole-file
    reports see no difference, a narrow attack window does."""
    whole_off = analyze.analyze(BELL_OP2OFF)
    whole_on = analyze.analyze(BELL_ALGO5)
    assert whole_off["spectral_centroid_hz"] == pytest.approx(
        whole_on["spectral_centroid_hz"], rel=0.1
    )

    attack_off = analyze.analyze(BELL_OP2OFF, window=(0.0, 0.02114))
    attack_on = analyze.analyze(BELL_ALGO5, window=(0.0, 0.02114))
    assert attack_on["spectral_centroid_hz"] > attack_off["spectral_centroid_hz"] + 200


# ---------------------------------------------------------------- known positives
# Added on promotion: a mutation run (clip threshold raised past full scale)
# left the V2 suite green, so each fault class the report claims to detect now
# has a signal that must trip it.

def test_bs1770_reference_level(tmp_path):
    """EBU Tech 3341 case: stereo 1 kHz sine at -23 dBFS reads -23 LUFS."""
    fs = 48000
    t = np.arange(fs * 10) / fs
    y = 10 ** (-23 / 20) * np.sin(2 * np.pi * 1000 * t)
    path = str(tmp_path / "ref.wav")
    write_wav_24bit(path, np.stack([y, y], axis=1), fs)
    assert analyze.analyze(path)["lufs_integrated"] == pytest.approx(-23.0, abs=0.1)


def test_clipping_is_counted(tmp_path):
    fs = 44100
    t = np.arange(fs) / fs
    y = np.clip(1.5 * np.sin(2 * np.pi * 100 * t), -1.0, 1.0)
    path = str(tmp_path / "clipped.wav")
    write_wav_24bit(path, np.stack([y, y], axis=1), fs)
    assert analyze.analyze(path)["clipped_samples"] > 1000


def test_true_peak_exceeds_sample_peak_for_intersample_overs(tmp_path):
    """fs/4 sine sampled at 45 degrees: every sample sits at 0.707 of the
    waveform's real peak, so true peak must read ~3 dB above sample peak."""
    fs = 44100
    n = np.arange(fs)
    y = 0.9 * np.sin(np.pi / 2 * n + np.pi / 4)
    path = str(tmp_path / "isp.wav")
    write_wav_24bit(path, np.stack([y, y], axis=1), fs)
    r = analyze.analyze(path)
    assert r["true_peak_dbtp"] - r["sample_peak_dbfs"] > 2.5


def test_silence_run_and_mono_collapse_are_reported(tmp_path):
    fs = 44100
    t = np.arange(fs) / fs
    tone = 0.5 * np.sin(2 * np.pi * 440 * t)
    y = np.concatenate([tone, np.zeros(fs), tone])
    path = str(tmp_path / "gap.wav")
    write_wav_24bit(path, np.stack([y, -y], axis=1), fs)   # polarity-inverted: cancels in mono
    r = analyze.analyze(path)
    assert any(0.9 <= s <= 1.1 for s in r["silence_runs_ge_0.5s"])
    assert r["stereo_correlation"] == pytest.approx(-1.0, abs=0.01)
