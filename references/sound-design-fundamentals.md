# Sound design fundamentals

Tier tags follow `evidence-status.md`. Much of this is SOURCE-BACKED
concept from the V2 corpus. Project proof is narrow and is marked where it
exists. Synthesis knowledge beyond what is tagged here is a recorded gap,
not something to improvise and present as package guidance.

## Sound as manipulable dimensions — SOURCE-BACKED (V2 corpus §1)

Most production work manipulates a small set of dimensions:
source/spectrum, pitch/phase, amplitude/envelope, frequency balance, time,
modulation, stereo, space, nonlinearity, structure (routing, buses,
automation) and iteration (render → manipulate → render). The compact
working vocabulary: generate, select, layer, tune, envelope, filter,
modulate, distort, compress, equalise, time-shift, pitch, stretch,
resample, spatialise, route, automate, measure, compare.

## Choosing a synthesis route — SOURCE-BACKED (V2 corpus §2)

| Need | Likely route |
|---|---|
| Predictable bass, lead, pluck, pad or analogue-style tone | **Subtractive**: harmonically rich oscillator → filter → amp |
| Metallic, bell-like or complex digital timbres, aggressive growls | **FM/PM**: carrier/modulator ratio sets the harmonic structure, index sets complexity, and enveloping the modulator lets a sound go from complex to simple |
| The oscillator's harmonic structure itself must move | **Wavetable** (or FM/granular) |
| Precise harmonic composition; reasoning in partials rather than "warmth" | **Additive** (a lower priority for ordinary production) |
| Textures, frozen sounds, decoupling pitch from time, new instruments from recordings | **Granular**, as part of the transformation toolbox |

The key distinction to make: *"I need brightness movement"* (filter
modulation may be enough) versus *"I need the harmonic structure to
mutate"* (wavetable/FM/granular).

**Internal evidence:** only subtractive (filter-LFO wobble, sine sub,
unison saw) and **one bounded FM case** have been exercised. Wavetable,
granular and additive are NOT YET COVERED internally.

### The bounded FM case — PROJECT-PROVEN, one voice (V2 `designed-sound-palette-01`)

- The voice was a 2-operator FM bell/pluck programmed from init, not a
  preset. Carrier ratio 1.0; modulator ratio ≈3.35 with a fast attack and
  fast decay; other operators off.
- **The first routing assumption was wrong.** On the first algorithm
  chosen, an A/B render with the modulator off and on showed *zero*
  difference. The modulator was not reaching the carrier. The lesson is
  portable: in any operator-based synth, verify that the modulator is
  actually routed into the carrier by rendering with it on and off before
  designing around it. Don't infer routing from a diagram or an assumption.
- On the corrected routing, whole-file metrics *still* showed no
  difference. A 21 ms attack window showed the FM signature: centroid about
  2980 Hz decaying to about 724 Hz over 200 ms with the modulator, versus a
  flat ~420 Hz without it. That is a bright inharmonic transient decaying
  into the pure carrier. **Verify transient design elements in a window**
  (`analyze.py --window`), not with whole-file aggregates.
- The palette containing this voice passed a human verdict. The listener
  named its interesting individual sounds.
- **What this does not prove:** general FM design, ratio families, feedback,
  multi-operator stacks, FM basses or index automation. Those stay
  SOURCE-BACKED (V2 corpus §2; the V1 bass playbook cites high-index FM plus
  bit reduction for dirty mid-bass) until exercised.

## Oscillators, unison, noise — BOTH, with a preserved disagreement

| Need | Likely source (SOURCE-BACKED, V2 corpus §3) |
|---|---|
| Pure sub | Sine |
| Slightly more audible sub | Triangle, or a saturated sine |
| Bright subtractive bass | Saw |
| Hollow/reedy | Pulse |
| Attack/click | Noise or a very short transient |
| Air/hiss | Filtered noise |
| Wide supersaw | Several detuned saws |

Unison is not "better". It trades precision for density and width.

**OPEN / DISAGREEMENT (preserve it):** does oscillator detune add richness
or dilute clarity?

- One practitioner source recommends detune (1–10%), vibrato LFO,
  independent wavetable-position LFO and unison spread for pads [Ableton,
  "Pad It Out"].
- Another argues detune clouds pitch clarity and prefers rhythmic
  step-modulation, wave-sequencing and slow level changes [SOS, "Creating &
  Using Synth Pad Sounds"].
- Both agree that layering *genuinely different sources* adds complexity
  without clouding the fundamental.

**Internal measurement (PROJECT-PROVEN, V1 Study 4):** two centred,
layered sources rendered **perfectly mono (correlation 1.000)**, while one
heavily detuned unison voice rendered wide (0.400). Layering alone does not
create width; width has to be engineered. The same study's listener
preferred the unison version for one warm target sound. That is **HUMAN
PREFERENCE (single instance)** and does not settle the disagreement above.

## Envelopes and modulation — PARTIAL

- Distinguish the sources [SOURCE-BACKED, V2 corpus §4]: **envelope** =
  change relative to an event; **LFO** = cyclic change; **envelope
  follower** = change derived from another signal; **automation** = change
  relative to the composition; **random** = controlled variation.
  Envelopes can drive filter cutoff, pitch, FM index, wavetable position,
  distortion amount and sends, not only amplitude.
- Controlled modulation, rather than more notes, keeps repeated electronic
  material from sounding identical [SOURCE-BACKED].
- An LFO delay (the wobble not starting at note-on) is part of the classic
  wobble sound. LFOs may be tempo-synced or free-running; synced suits
  dance-floor sections, free-running suits atmospheric material.
  [SOURCE-BACKED: MusicRadar; Surge XT manual — weaker tutorial-tier
  evidence for the rate/feel claims]
- Two independently rated modulators on different targets (e.g. pitch
  depth and timbre position) avoid both a static sound and lockstep
  movement [SOURCE-BACKED; untested internally].

## Filters — PARTIAL

Functional vocabulary [SOURCE-BACKED, V2 corpus §5]: LP darkens, HP thins,
BP isolates, notch rejects, shelf balances broadly, resonance accents
movement/formants, comb colours with pitch. Cutoff can be driven by an
envelope, LFO, velocity, key tracking, another audio signal or automation.
"Make it more alive" often calls for controlled filter or timbre movement
rather than another layer. Dedicated filter-design knowledge (types,
resonance behaviour) is NOT YET COVERED internally.

## Two different kinds of bass movement — BOTH

- **Filter-LFO wobble**: an LFO (or LFO-shaped envelope) moving a low-pass
  cutoff, usually with distortion/compression after it for the genre
  character [SOURCE-BACKED: MusicRadar].
- **Reese movement**: phase-cancellation beating between 2–3 detuned
  oscillators, with no LFO required. The detune amount sets the beat rate.
  [SOURCE-BACKED: Attack Magazine "Reese Bass Redux"]
- **PROJECT-PROVEN (V1 Study 1, human verdict):** both were built on
  identical material and judged strong, distinctive, and *mechanically
  different* kinds of movement. Neither ranked above the other. Plain
  note-level bass writing also worked, but sounded more basic in that
  instance. Don't conflate the two mechanisms.

## Saturation inside a patch vs on a bus

Saturation that builds a patch's character (e.g. a distortion stage on a
mid-bass voice) belongs here. Saturation that balances an existing track or
bus belongs in `mixing-and-mastering`. The mechanism is the same; the
question is whether you are building the sound or balancing it. Order
matters either way: filter → distortion ≠ distortion → filter. Try both
rather than assuming [SOURCE-BACKED, V2 corpus §9]. See
`mixing-dynamics-and-spatial.md` for the saturation evidence.

## Layer by function, not quantity — SOURCE-BACKED; PROJECT-PROVEN once

Give each layer one job, then remove redundancy (V2 corpus §18):
bass = sub (weight) + mid-bass (identity) + texture + stereo top (size);
pad = centre (harmony) + wide layer + noise/air.
`designed-sound-palette-01` built five instruments each assigned a
distinct role, and confirmed by solo renders that they had measurably
distinct spectral identities. The palette passed a human verdict.

## When a source keeps failing: change class — PROJECT-PROVEN (V2)

Two rejections of sources in the *same class* signal a class change, not a
third preset. V2's piano search went synth preset → FM voice → General MIDI
soundfont → real sampled instrument, each step a change of class. The
listener accepted the final sampled instrument. The heuristic generalises
to any sound-source search.

## Pads and found material — BOTH / SOURCE-BACKED

- Found or organic material adds humanity through restraint and contrast:
  keep it filtered or ducked under other material, and place discrete hits
  at punctuation points [SOURCE-BACKED: Attack Magazine "Lo-Fi Sound"].
- Don't reprocess material that is already characterful; leaving
  bleed/room noise is often what makes a sample work [SOURCE-BACKED].
- The pad measurements above (V1 Study 4) are the internal evidence.

## Not covered

Leads/plucks as a voice type, filter design, transient shaping, and
wavetable/granular/additive practice. See `evidence-status.md`.
