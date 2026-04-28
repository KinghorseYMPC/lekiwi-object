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
6. Prefer small stages. Each new stage should leave runnable code, docs, and a git commit.

## Current Architecture

The initial skeleton is intentionally conservative:

- `lekiwi_object.workflow` coordinates agents.
- `lekiwi_object.agents.voice_agent` parses text commands as the first local stand-in for speech.
- `lekiwi_object.agents.vision_agent` provides simulated scene observations, with room for camera/VLM backends.
- `lekiwi_object.agents.control_agent` maps intents to safe dry-run control commands.
- `lekiwi_object.tools.check_ssh` verifies Raspberry Pi SSH reachability without storing credentials.

## Suggested Development Stages

1. Stage 0: repository hygiene, docs, local dry-run workflow.
2. Stage 1: SSH and LeKiwi host startup checklist.
3. Stage 2: local text command workflow with real LeKiwi observation stream.
4. Stage 3: microphone ASR and TTS.
5. Stage 4: visual recognition and target tracking.
6. Stage 5: safe object touch primitive.
7. Stage 6: demo polish and robustness.

