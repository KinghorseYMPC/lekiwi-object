# Prerequisites For Hardware Stages

These items are not separate goals from `guideline.md`. They are required preparation for the stage-one workflow to work on the real LeKiwi robot.

## Hand-Eye Calibration

Purpose: support visual target localization for object touch.

Local implementation:

- `CameraIntrinsics`
- `HandEyeCalibration`
- `CalibrationGate`

Current status:

- Missing or placeholder calibration is explicitly marked incomplete.
- Touch plans remain blocked until camera intrinsics, camera-to-end-effector transform, and reprojection error are available.

## Visual Recognition Preparation

Purpose: move from pure simulation toward real camera/VLM recognition without opening the laptop camera.

Local implementation:

- `VisionTargetRegistry`
- `SampleFileVisionBackend`
- `samples/vision/desk_scene.json`

Current status:

- Common targets are normalized: computer screen, switch, button, face/person.
- Sample JSON can test recognition output shape before Raspberry Pi camera integration.
- Laptop camera remains forbidden.

## Object Touch Preparation

Purpose: make touch execution conditional on safety and geometry readiness.

Local implementation:

- `TouchPlanner`
- `TouchPlan`

Current status:

- Touch requests produce a dry-run plan.
- The plan lists missing prerequisites such as calibration or depth.
- Physical touch is still blocked.

## Voice Interaction Preparation

Purpose: test fuzzy Chinese command coverage before real ASR/TTS.

Local implementation:

- `VoiceCommandExample`
- `VoicePrerequisiteEvaluator`

Current status:

- Baseline Chinese commands cover scene recognition, tracking, touch, stop, and chat.
- The evaluator can catch regressions in intent routing.

