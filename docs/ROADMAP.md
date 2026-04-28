# Roadmap

## Stage 0: Local Dry-Run Skeleton

Goal: make the project cloneable and runnable by a teammate without hardware.

Acceptance:

- `python -m lekiwi_object.cli --text "看一下桌面" --dry-run` works.
- README explains GitHub setup.
- AGENTS/SKILLS document future Codex workflow.

## Stage 1: Robot Connectivity

Goal: verify laptop-to-Pi connectivity and document the minimal Pi-side process.

Acceptance:

- SSH reachability check works.
- Pi host startup command is documented.
- No password or secret is stored in git.

## Stage 2: Observation Stream

Goal: receive front/wrist camera frames and robot state on the laptop.

Acceptance:

- LeKiwi client connects to the Pi host.
- A local script prints state keys and frame sizes.
- Dry-run commands remain the default.

## Stage 3: Voice Interaction

Goal: replace text input with microphone ASR and spoken replies.

Acceptance:

- Chinese voice commands map to intents.
- The system can reply by TTS.
- Text mode remains available for debugging.

## Stage 4: Vision Recognition And Tracking

Goal: support scene description and target centering.

Acceptance:

- "我正在电脑上做什么" returns a visual description.
- "看我的电脑屏幕" tracks a selected object in the wrist camera.
- Tracking commands are rate-limited and safe.

## Stage 5: Object Touch

Goal: implement a cautious touch primitive for one selected object class.

Acceptance:

- The system estimates a reachable target point.
- The arm moves in small guarded steps.
- The workflow can abort safely.

