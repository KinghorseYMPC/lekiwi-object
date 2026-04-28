# Offline Development

This stage intentionally avoids real SSH and hardware motion.

## What We Can Build Locally

- Text-mode voice agent for Chinese commands.
- Mock ASR/TTS wiring for the complete voice interaction shape.
- Intent routing for chat, scene description, tracking, touch, and stop.
- Explicit function calls from voice intent to agent capabilities.
- Task state tracking for running, completed, and blocked workflows.
- Replaceable vision backend interface.
- Camera source policy that forbids laptop camera use.
- Simulated vision observations with image-space target boxes.
- Closed-loop tracking simulation.
- Safety-limited control command generation.
- Centralized control safety review.
- Dry-run command execution backend.
- Tests that run on a teammate's laptop after cloning from GitHub.

## What We Are Not Claiming Yet

- The Raspberry Pi is reachable.
- The LeKiwi host process starts correctly.
- Real cameras stream frames.
- The motors move in the expected direction.
- The robot can safely touch a real object.

## Useful Commands

Scene description:

```bash
python -m lekiwi_object.cli --text "看一下桌面" --dry-run
```

Voice-loop shape with wake word:

```bash
python -m lekiwi_object.cli --text "小车，看一下桌面" --dry-run --json
```

Tracking loop:

```bash
python -m lekiwi_object.cli --text "看我的电脑屏幕" --dry-run --steps 6
```

Touch planning safety check:

```bash
python -m lekiwi_object.cli --text "碰一下那个开关" --dry-run --json
```

Tests:

```bash
python -m pytest -q -p no:cacheprovider
```

## Implementation Notes

- `OfflineWorld` owns simulated target positions.
- `MockSpeechIO` provides local mock ASR/TTS without microphone or speaker access.
- `FunctionRouter` turns parsed voice intent into workflow calls.
- `VisionBackend` defines the future camera/VLM integration point.
- `CameraSourcePolicy` rejects laptop/local webcam sources.
- `OfflineVisionBackend` adapts `OfflineWorld` to the vision-agent contract.
- `SimulatedVisionAgent` turns world state into observations.
- `DryRunControlAgent` turns observations into safe commands.
- `ControlSafetyLayer` rejects commands that exceed configured limits or attempt unsafe live motion.
- `DryRunRobotBackend` records commands and never contacts the Pi.
- `TaskStateTracker` summarizes progress for user-facing feedback.
- `MultiAgentWorkflow.run_text_loop(..., steps=N)` links these pieces into a local feedback loop.

## Camera Boundary

The USB camera used for the project is connected directly to the Raspberry Pi. It may be fixed to the follower arm or removed from the arm, but it remains robot-side hardware.

The laptop camera is forbidden for privacy reasons. Offline development must use `offline_world` or explicit sample files. Later hardware development may use `raspberry_pi_usb` after SSH and LeKiwi host setup are approved.
