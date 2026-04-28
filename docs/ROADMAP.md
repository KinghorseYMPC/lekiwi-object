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

## Stage 2: Robot Connectivity

Goal: verify laptop-to-Pi connectivity and document the minimal Pi-side process.

Acceptance:

- SSH reachability check works.
- Pi host startup command is documented.
- No password or secret is stored in git.

## Stage 3: Observation Stream

Goal: receive front/wrist camera frames and robot state on the laptop.

Acceptance:

- LeKiwi client connects to the Pi host.
- A local script prints state keys and frame sizes.
- Dry-run commands remain the default.

## Stage 4: Voice Interaction

Goal: replace text input with microphone ASR and spoken replies.

Acceptance:

- Chinese voice commands map to intents.
- The system can reply by TTS.
- Text mode remains available for debugging.

## Stage 5: Vision Recognition And Tracking

Goal: support scene description and target centering.

Acceptance:

- "我正在电脑上做什么" returns a visual description.
- "看我的电脑屏幕" tracks a selected object in the wrist camera.
- Tracking commands are rate-limited and safe.

## Stage 6: Object Touch

Goal: implement a cautious touch primitive for one selected object class.

Acceptance:

- The system estimates a reachable target point.
- The arm moves in small guarded steps.
- The workflow can abort safely.
