# lekiwi object

Local-first multi-agent project for the LeKiwi mobile manipulator course demo.

The course goal is a working loop:

```text
voice request -> intent routing -> vision context -> LeKiwi control -> feedback
```

This repository starts with a safe laptop-side skeleton. It runs in dry-run mode first, so we can iterate without moving the real robot until the SSH, camera, and safety checks are ready.

## Current Scope

Implemented in this initial stage:

- project docs for future Codex sessions;
- offline speech I/O structure with mock ASR and mock TTS;
- local multi-agent workflow skeleton;
- fuzzy text intent routing for Chinese commands;
- explicit function calls from voice-agent intent to vision/control tasks;
- task states for running, completed, and blocked workflows;
- replaceable vision backend interface for scene understanding and tracking;
- camera source policy that forbids laptop camera use;
- simulated vision observations and a multi-step offline world;
- dry-run control command generation;
- centralized control safety layer for speed, duration, live-motion, and guarded-touch checks;
- dry-run robot backend that records commands without SSH or robot motion;
- SSH reachability checker for the Raspberry Pi;
- project-level git setup plan.

Not implemented yet:

- real microphone ASR/TTS;
- live LeKiwi ZMQ client integration;
- real camera/VLM perception;
- calibrated target touching.

## Quick Start

From this folder:

```bash
python -m lekiwi_object.cli --text "看一下桌面" --dry-run
python -m lekiwi_object.cli --text "看我的电脑屏幕" --dry-run
python -m lekiwi_object.cli --text "碰一下那个开关" --dry-run
```

Expected behavior: the CLI prints a parsed intent, a vision observation, a dry-run control command, and a Chinese response.

The output also shows:

- the simulated speech-recognition input;
- the function call selected by the voice interaction agent;
- the current task state;
- the dry-run execution backend result.
- the simulated speech-synthesis output.
- the control safety review status and violations.

Run a local closed-loop tracking simulation:

```bash
python -m lekiwi_object.cli --text "看我的电脑屏幕" --dry-run --steps 6
```

Expected behavior: each step observes the simulated target, emits a safe centering command, records it locally, and updates the offline world so the target moves toward the image center.

## Raspberry Pi SSH Check

Known connection:

```bash
ssh gjy@rasberrypi16.local
```

Do not store the password in this repository. To check connectivity:

```bash
python -m lekiwi_object.tools.check_ssh --host rasberrypi16.local --user gjy
```

For key-based non-interactive checking:

```bash
python -m lekiwi_object.tools.check_ssh --host rasberrypi16.local --user gjy --batch
```

## Local-First Design

The Raspberry Pi should do the minimum necessary hardware work:

- run the LeKiwi host process;
- stream observations;
- execute final base/arm commands.

The laptop should do heavier logic:

- speech recognition and reply generation;
- intent routing;
- VLM/object detection;
- task planning;
- safety checks and command shaping.

This matches the existing LeRobot LeKiwi pattern in the parent repository: Raspberry Pi host plus laptop client over ZMQ.

## Offline Development Boundary

This repository can make useful progress without real SSH:

- intent parsing;
- offline ASR/TTS interface wiring;
- workflow state and task routing;
- automatic function calls such as `vision.track_target` and `manipulation.touch_target`;
- task status tracking for closed-loop progress;
- simulated scene recognition;
- simulated target tracking;
- replaceable vision backend wiring for future camera/VLM integration;
- camera source policy for offline, sample-file, or Raspberry Pi USB cameras only;
- safety rules and dry-run command execution;
- centralized command safety review before backend execution;
- tests and GitHub collaboration.

Real SSH or hardware is still required for:

- confirming `rasberrypi16.local` is reachable;
- starting the LeKiwi host process on the Pi;
- receiving real camera frames;
- verifying motor IDs, directions, limits, and latency;
- validating any physical touch behavior.

## Camera Privacy Policy

This project must not open or use the laptop camera.

Allowed visual inputs:

- `offline_world`: deterministic simulation, no physical camera.
- `sample_file`: explicit local sample file, no camera access.
- `raspberry_pi_usb`: USB camera directly connected to the Raspberry Pi, for later hardware stages.

Forbidden visual inputs:

- laptop camera;
- local webcam;
- OpenCV numeric camera indices on the laptop.

The default config keeps `vision.allow_laptop_camera` set to `false`. If a config tries to enable the laptop camera or sets `vision.source` to `laptop_camera`, the project raises an error before any camera code can run.

## GitHub Setup

This project folder is managed as its own git repository.

Recommended GitHub steps:

```bash
git init
git branch -M main
git add .
git commit -m "Initialize lekiwi object project skeleton"
git remote add origin https://github.com/<your-user>/lekiwi-object.git
git push -u origin main
```

Colleagues can then clone:

```bash
git clone https://github.com/<your-user>/lekiwi-object.git
cd lekiwi-object
python -m lekiwi_object.cli --text "看一下桌面" --dry-run
```

## Suggested Roadmap

1. Stage 0: dry-run workflow and repository hygiene.
2. Stage 1: offline simulator, safety backend, and closed-loop tests.
3. Stage 2: function calls and task state.
4. Stage 3: offline speech I/O with mock ASR/TTS.
5. Stage 4: SSH check and documented Pi host startup.
6. Stage 5: vision backend interface for future camera/VLM integration.
7. Stage 6: camera source privacy policy and Raspberry Pi USB camera boundary.
8. Stage 7: control safety layer for backend execution.
9. Stage 8: LeKiwi client observation stream on laptop.
10. Stage 9: real microphone ASR and TTS.
11. Stage 10: visual recognition and target tracking.
12. Stage 11: cautious object-touch primitive.
13. Stage 12: demo script, logging, and robustness pass.
