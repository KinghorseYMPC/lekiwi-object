from __future__ import annotations

import argparse
import subprocess


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check SSH reachability for the LeKiwi Raspberry Pi.")
    parser.add_argument("--host", default="rasberrypi16.local")
    parser.add_argument("--user", default="gjy")
    parser.add_argument("--batch", action="store_true", help="Fail fast instead of prompting for a password.")
    parser.add_argument("--timeout", type=int, default=8)
    args = parser.parse_args(argv)

    options = [
        "-o",
        f"ConnectTimeout={args.timeout}",
        "-o",
        "StrictHostKeyChecking=accept-new",
    ]
    if args.batch:
        options.extend(["-o", "BatchMode=yes"])

    target = f"{args.user}@{args.host}"
    command = ["ssh", *options, target, "printf", "lekiwi-ssh-ok"]
    print(f"Checking SSH target: {target}")

    try:
        completed = subprocess.run(command, check=False, text=True, capture_output=True, timeout=args.timeout + 5)
    except FileNotFoundError:
        print("ssh executable was not found on PATH.")
        return 2
    except subprocess.TimeoutExpired:
        print("SSH check timed out.")
        return 3

    if completed.returncode == 0 and "lekiwi-ssh-ok" in completed.stdout:
        print("SSH check passed.")
        return 0

    print("SSH check failed.")
    if completed.stderr:
        print(completed.stderr.strip())
    return completed.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())

