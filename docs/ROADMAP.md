# Roadmap

## Stage 0: Local Dry-Run Skeleton

Goal: make the project cloneable and runnable by a teammate without hardware.

Acceptance:

- `python -m lekiwi_object.cli --text "看一下桌面" --dry-run` works.
- README explains GitHub setup.
- AGENTS/SKILLS document future Codex workflow.

## Stage 1: Offline Simulator And Safety Backend

Goal: keep implementing the required multi-agent workflow without SSH or hardware.

Acceptance:

- `python -m lekiwi_object.cli --text "看我的电脑屏幕" --dry-run --steps 6` shows a target moving toward image center.
- The workflow records commands through a dry-run robot backend.
- Touch commands are blocked unless calibration is explicitly modeled.
- Unit tests cover intent routing, tracking convergence, and live-command rejection.

## Stage 2: Function Calls And Task State

Goal: make the voice interaction agent explicitly choose workflow capabilities, as required by `guideline.md`.

Acceptance:

- Scene requests route to `vision.describe_scene`.
- Tracking requests route to `vision.track_target`.
- Touch requests route to `manipulation.touch_target`.
- Stop requests route to `robot.stop`.
- Workflow output includes task status: `running`, `completed`, or `blocked`.

## Stage 3: Offline Speech I/O

Goal: represent the full voice-interaction flow required by `guideline.md` without needing microphone or speaker hardware.

Acceptance:

- Workflow output includes mock ASR input.
- Workflow output includes mock TTS output.
- Wake-word stripping can be simulated locally.
- Existing text command debugging remains available.

## Stage 4: Robot Connectivity

Goal: verify laptop-to-Pi connectivity and document the minimal Pi-side process.

Acceptance:

- SSH reachability check works.
- Pi host startup command is documented.
- No password or secret is stored in git.

## Stage 5: Vision Backend Interface

Goal: keep the vision agent aligned with `guideline.md` while making perception backends replaceable.

Acceptance:

- A `VisionBackend` contract exists.
- The offline world is exposed through `OfflineVisionBackend`.
- Workflow can receive a custom vision backend later without changing the voice/control loop.
- Tests cover backend delegation and metadata.

## Stage 6: Camera Source Privacy Boundary

Goal: enforce that project vision never opens the laptop camera, while leaving a path for the Raspberry Pi USB camera.

Acceptance:

- Config defaults to `vision.source = offline_world`.
- `vision.allow_laptop_camera = true` is rejected.
- `vision.source = laptop_camera` is rejected.
- `raspberry_pi_usb` is documented as the future robot-side camera source.
- Vision metadata records `opens_laptop_camera = false`.

## Stage 7: Control Safety Layer

Goal: align the mechanical control agent with `guideline.md` while preventing unsafe backend execution.

Acceptance:

- A `ControlSafetyLayer` reviews commands before any backend execution.
- Commands over speed or duration limits are rejected.
- Live commands are rejected while dry-run safety is enabled.
- Live guarded touch is blocked until explicit hardware-stage approval.
- Execution output includes safety status and violations.

## Stage 8: Offline Session Trace Export

Goal: preserve complete local workflow runs for debugging, teammate handoff, and course demo preparation.

Acceptance:

- CLI can write `--trace-jsonl logs/<name>.jsonl`.
- Trace export path must stay inside the project folder.
- Each record includes speech input, function call, vision observation, command, execution, safety review, task state, and speech output.
- Tests cover serialization and path validation.

## Stage 9: Observation Stream

Goal: receive front/wrist camera frames and robot state on the laptop.

Acceptance:

- LeKiwi client connects to the Pi host.
- A local script prints state keys and frame sizes.
- Dry-run commands remain the default.

## Stage 10: Real Voice Interaction

Goal: replace text input with microphone ASR and spoken replies.

Acceptance:

- Chinese voice commands map to intents.
- The system can reply by TTS.
- Text mode remains available for debugging.

## Stage 11: Vision Recognition And Tracking

Goal: support scene description and target centering.

Acceptance:

- "我正在电脑上做什么" returns a visual description.
- "看我的电脑屏幕" tracks a selected object in the wrist camera.
- Tracking commands are rate-limited and safe.

## Stage 12: Object Touch

Goal: implement a cautious touch primitive for one selected object class.

Acceptance:

- The system estimates a reachable target point.
- The arm moves in small guarded steps.
- The workflow can abort safely.
