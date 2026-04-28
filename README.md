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
- local multi-agent workflow skeleton;
- fuzzy text intent routing for Chinese commands;
- simulated vision observations;
- dry-run control command generation;
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
2. Stage 1: SSH check and documented Pi host startup.
3. Stage 2: LeKiwi client observation stream on laptop.
4. Stage 3: microphone ASR and TTS.
5. Stage 4: visual recognition and target tracking.
6. Stage 5: cautious object-touch primitive.
7. Stage 6: demo script, logging, and robustness pass.

