from __future__ import annotations

import argparse
import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any

from lekiwi_object.config import load_config
from lekiwi_object.workflow import MultiAgentWorkflow


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the local LeKiwi object multi-agent workflow.")
    parser.add_argument("--config", default=None, help="Path to a JSON config file.")
    parser.add_argument("--text", required=True, help="Text command used as the current speech stand-in.")
    parser.add_argument("--dry-run", action="store_true", help="Keep robot commands in dry-run mode.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args(argv)

    config = load_config(args.config)
    if args.dry_run and not config.safety.dry_run:
        raise SystemExit("Refusing to override a live config from the CLI skeleton. Use a config file intentionally.")

    result = MultiAgentWorkflow(config).run_text(args.text)
    if args.json:
        print(json.dumps(_to_jsonable(result), ensure_ascii=False, indent=2))
    else:
        _print_human(result)
    return 0


def _print_human(result: Any) -> None:
    print("Intent:")
    print(f"  type: {result.intent.type.value}")
    print(f"  target: {result.intent.target}")
    print(f"  confidence: {result.intent.confidence}")
    print("Vision:")
    print(f"  summary: {result.observation.summary}")
    print(f"  bbox_xywh: {result.observation.bbox_xywh}")
    print("Control:")
    print(f"  command: {result.command.name}")
    print(f"  dry_run: {result.command.dry_run}")
    print(f"  parameters: {result.command.parameters}")
    print("Response:")
    print(f"  {result.response}")


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: _to_jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {key: _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(item) for item in value]
    return value


if __name__ == "__main__":
    raise SystemExit(main())

