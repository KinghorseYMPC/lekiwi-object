# Guideline Traceability

This file maps the local implementation to the requirements in `guideline.md`.

`guideline.md` is the source of truth and should not be modified.

## Required Multi-Agent Roles

Voice interaction agent:

- Current local implementation: `TextVoiceAgent`
- Current local I/O: `MockSpeechIO`
- Current capability: mock ASR, Chinese command parsing, reply text generation, mock TTS output.
- Next capability: microphone ASR, response generation, and TTS.

Vision agent:

- Current local implementation: `SimulatedVisionAgent` plus `OfflineWorld`
- Current backend contract: `VisionBackend`
- Current backend implementation: `OfflineVisionBackend`
- Current camera policy: laptop camera is forbidden; allowed sources are offline simulation, sample files, or Raspberry Pi USB camera.
- Current capability: scene description, target bounding boxes, target offsets, touch target metadata.
- Next capability: real camera frames and VLM/object detection.

Mechanical control agent:

- Current local implementation: `DryRunControlAgent`
- Current safety implementation: `ControlSafetyLayer`
- Current capability: safe command planning for no-motion, target centering, stop, and blocked touch.
- Next capability: LeKiwi ZMQ client backend after SSH/host verification.

## Required Stage-One Functions

Voice interaction:

- Current status: text-mode local proxy plus mock ASR/TTS exists.
- Verification: `python -m lekiwi_object.cli --text "小车，看一下桌面" --dry-run --json`
- Remaining: real ASR and TTS.

Visual scene recognition:

- Current status: offline simulated scene recognition exists.
- Verification: `python -m lekiwi_object.cli --text "看一下桌面" --dry-run`
- Remaining: real camera/VLM backend.

Face or object tracking:

- Current status: offline closed-loop tracking simulation exists.
- Verification: `python -m lekiwi_object.cli --text "看我的电脑屏幕" --dry-run --steps 6`
- Remaining: real wrist-camera feedback and physical arm/base motion.

Object touch:

- Current status: request parsing, visual target localization, and safety blocking exist.
- Verification: `python -m lekiwi_object.cli --text "碰一下那个开关" --dry-run --json`
- Remaining: hand-eye calibration, guarded motion planning, and hardware validation.

## Hardware Prerequisites

The following local modules support `guideline.md` but do not replace real hardware validation:

- `calibration.py`: checks whether hand-eye calibration data is complete.
- `vision_targets.py` and `SampleFileVisionBackend`: prepare target definitions and sample-file recognition before the Raspberry Pi USB camera is used.
- `touch_planning.py`: creates a dry-run touch plan and lists missing prerequisites.
- `voice_prerequisites.py`: checks baseline Chinese command coverage before real ASR/TTS.

## Function Calling

The voice-side router currently emits:

- `chat.respond`
- `vision.describe_scene`
- `vision.track_target`
- `manipulation.touch_target`
- `robot.stop`

This keeps the workflow aligned with the requirement that the interaction agent decides which capability to call.

## Offline Traceability

The CLI can export one JSONL record per workflow step:

```bash
python -m lekiwi_object.cli --text "看我的电脑屏幕" --dry-run --steps 6 --trace-jsonl logs/demo_trace.jsonl
```

Each record preserves the full local chain from mock speech input through function calling, vision observation, control planning, safety review, dry-run execution, task status, and mock speech output. This supports the stage-one requirement that the system form a complete workflow loop before hardware validation.

## Explicit Non-Goals Before User Approval

- No real SSH connection.
- No Raspberry Pi file changes.
- No live robot motion.
- No laptop camera access.
- No stored password or secret.
