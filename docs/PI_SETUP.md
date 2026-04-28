# Raspberry Pi Minimal Setup

This project should keep Pi-side work small. The laptop runs the agents; the Pi runs the LeKiwi hardware host.

## Known SSH

```bash
ssh gjy@rasberrypi16.local
```

Do not commit the password. Prefer setting up SSH keys later.

## Connectivity Check

From this folder:

```bash
python -m lekiwi_object.tools.check_ssh --host rasberrypi16.local --user gjy
```

If you have SSH keys configured:

```bash
python -m lekiwi_object.tools.check_ssh --host rasberrypi16.local --user gjy --batch
```

## LeKiwi Host Reference

The parent repository contains:

```text
src/lerobot/robots/lekiwi/lekiwi_host.py
src/lerobot/robots/lekiwi/lekiwi_client.py
src/lerobot/robots/lekiwi/config_lekiwi.py
```

The host binds:

- command port: `5555`
- observation port: `5556`

The laptop client connects to those ports.

## Safety Notes

- Keep wheels lifted or the robot in a clear area for first live tests.
- Start with low speed and short duration.
- Keep an immediate power-off path.
- Keep dry-run on until the command path is understood.

