# SKILLS.md

Use this file as the project playbook for future Codex sessions.

## Skill: Project Orientation

When starting a new session:

1. Read `README.md`, `AGENTS.md`, and `guideline.md`.
2. Run `git status --short` inside this folder.
3. Run the local dry-run smoke test:

```bash
python -m lekiwi_object.cli --text "看一下桌面" --dry-run
```

## Skill: Safe Robot Work

Before any live robot command:

1. Confirm the robot is physically safe to move.
2. Confirm the follower arm and base have been calibrated.
3. Confirm the Raspberry Pi host process is running.
4. Confirm `--dry-run` is not being removed accidentally.
5. Use short durations and low speed first.

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

