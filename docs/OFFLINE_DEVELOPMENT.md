# Offline Development

This stage intentionally avoids real SSH and hardware motion.

## What We Can Build Locally

- Text-mode voice agent for Chinese commands.
- Intent routing for chat, scene description, tracking, touch, and stop.
- Explicit function calls from voice intent to agent capabilities.
- Task state tracking for running, completed, and blocked workflows.
- Simulated vision observations with image-space target boxes.
- Closed-loop tracking simulation.
- Safety-limited control command generation.
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
- `FunctionRouter` turns parsed voice intent into workflow calls.
- `SimulatedVisionAgent` turns world state into observations.
- `DryRunControlAgent` turns observations into safe commands.
- `DryRunRobotBackend` records commands and never contacts the Pi.
- `TaskStateTracker` summarizes progress for user-facing feedback.
- `MultiAgentWorkflow.run_text_loop(..., steps=N)` links these pieces into a local feedback loop.
