# SKILLS.md

Use this file as the project playbook for future Codex sessions.

## Skill: Project Orientation

When starting a new session:

1. Read `README.md`, `AGENTS.md`, and `guideline.md`.
2. Run `git status --short` inside this folder.
3. Run the local dry-run smoke test:

```bash
python -m lekiwi_object.cli --text "看一下桌面" --dry-run
python -m lekiwi_object.cli --text "小车，看一下桌面" --dry-run --json
python -m lekiwi_object.cli --text "看我的电脑屏幕" --dry-run --steps 6
```

## Skill: Safe Robot Work

Before any live robot command:

1. Confirm the robot is physically safe to move.
2. Confirm the follower arm and base have been calibrated.
3. Confirm the Raspberry Pi host process is running.
4. Confirm `--dry-run` is not being removed accidentally.
5. Use short durations and low speed first.

## Skill: Camera Privacy

The project must never use the laptop camera.

Allowed sources:

- `offline_world`
- `sample_file`
- `raspberry_pi_usb`

Useful check:

```bash
python -m lekiwi_object.cli --text "看一下桌面" --dry-run --json
```

Expected metadata includes:

- `camera_source: offline_world`
- `opens_laptop_camera: false`

## Skill: Offline Simulation

Use this while SSH or hardware is unavailable:

```bash
python -m lekiwi_object.cli --text "看我的电脑屏幕" --dry-run --steps 6
python -m lekiwi_object.cli --text "碰一下那个开关" --dry-run --json
python -m pytest -q -p no:cacheprovider
```

Expected result:

- tracking offsets shrink over multiple steps;
- mock ASR and mock TTS fields appear in CLI JSON output;
- touch commands remain blocked unless calibration is explicitly modeled;
- each workflow result includes the chosen function call and task state;
- vision observations include the active `vision_backend`;
- vision observations show `opens_laptop_camera: false`;
- execution backend is `dry_run`, meaning no SSH and no robot motion.

## Skill: Raspberry Pi SSH Check

The known SSH target is:

```bash
ssh gjy@rasberrypi16.local
```

Do not store the password in git. For checks from this project, use:

```bash
python -m lekiwi_object.tools.check_ssh --host rasberrypi16.local --user gjy
```

For non-interactive key-based checks:

```bash
python -m lekiwi_object.tools.check_ssh --host rasberrypi16.local --user gjy --batch
```

## Skill: GitHub Collaboration

Target repository name: `lekiwi object`.

Recommended GitHub repository slug: `lekiwi-object` because spaces in repo names are awkward for CLI tools.
The README keeps the visible project title as `lekiwi object`.

When publishing:

1. Create an empty GitHub repository.
2. Add it as `origin`.
3. Push the local `main` branch.
4. Ask colleagues to clone it and start from `README.md` plus `AGENTS.md`.
