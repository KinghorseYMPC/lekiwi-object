# AGENTS.md

This project is a local-first multi-agent controller for a LeKiwi mobile manipulator.
All generated project files must stay inside this `lekiwi object` folder.

## Mission

Build the course project described in `guideline.md`:

- voice interaction agent: speech input, intent routing, spoken response;
- vision agent: scene understanding, detection, target tracking;
- control agent: safe base and arm commands for LeKiwi;
- workflow: voice request -> vision context -> control action -> feedback loop.

## Working Rules For Codex

1. Do not edit, delete, or move files outside this folder.
2. You may read files outside this folder for reference, especially:
   - `src/lerobot/robots/lekiwi/`
   - `voice_control/`
   - `vision_control/`
   - `landmark/`
3. Keep Raspberry Pi changes minimal. Prefer laptop-side code and dry-run simulation first.
4. Never commit secrets. Do not write the Raspberry Pi password into tracked files.
5. Before hardware motion, keep `safety.dry_run` enabled until the user explicitly asks for live control.
6. Never open or use the laptop camera. Visual input may only come from offline simulation, explicit sample files, or the USB camera directly connected to the Raspberry Pi.
7. Prefer small stages. Each new stage should leave runnable code, docs, and a git commit.

## Current Architecture

The initial skeleton is intentionally conservative:

- `lekiwi_object.workflow` coordinates agents.
- `lekiwi_object.speech_io` provides offline mock ASR/TTS for the voice interaction loop.
- `lekiwi_object.agents.voice_agent` parses text commands as the first local stand-in for speech.
- `lekiwi_object.function_calling` converts voice intent into explicit function calls.
- `lekiwi_object.task_state` tracks whether a task is running, completed, or blocked.
- `lekiwi_object.simulation` provides an offline world for multi-step tracking tests.
- `lekiwi_object.camera_sources` enforces the laptop-camera privacy ban.
- `lekiwi_object.vision_backends` defines the backend contract for future camera/VLM work.
- `lekiwi_object.agents.vision_agent` reads simulated observations, with room for camera/VLM backends.
- `lekiwi_object.agents.control_agent` maps intents to safe dry-run control commands.
- `lekiwi_object.backends` records dry-run commands locally and blocks live execution in offline mode.
- `lekiwi_object.tools.check_ssh` verifies Raspberry Pi SSH reachability without storing credentials.

## Suggested Development Stages

1. Stage 0: repository hygiene, docs, local dry-run workflow.
2. Stage 1: offline simulator, safety backend, and closed-loop tests.
3. Stage 2: function calls and task state.
4. Stage 3: local speech I/O interface with mock ASR/TTS.
5. Stage 4: SSH and LeKiwi host startup checklist.
6. Stage 5: vision backend interface for future camera/VLM integration.
7. Stage 6: camera source privacy policy and Raspberry Pi USB camera boundary.
8. Stage 7: local text command workflow with real LeKiwi observation stream.
9. Stage 8: microphone ASR and TTS.
10. Stage 9: visual recognition and target tracking.
11. Stage 10: safe object touch primitive.
12. Stage 11: demo polish and robustness.
