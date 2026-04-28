from __future__ import annotations

import argparse
import json
from typing import Any

from lekiwi_object.config import load_config
from lekiwi_object.trace_export import trace_to_records, write_trace_jsonl
from lekiwi_object.workflow import MultiAgentWorkflow


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the local LeKiwi object multi-agent workflow.")
    parser.add_argument("--config", default=None, help="Path to a JSON config file.")
    parser.add_argument("--text", required=True, help="Text command used as the current speech stand-in.")
    parser.add_argument("--dry-run", action="store_true", help="Keep robot commands in dry-run mode.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--steps", type=int, default=1, help="Number of offline closed-loop simulation steps.")
    parser.add_argument("--trace-jsonl", default=None, help="Write workflow trace JSONL under this project folder.")
    args = parser.parse_args(argv)

    config = load_config(args.config)
    if args.dry_run and not config.safety.dry_run:
        raise SystemExit("Refusing to override a live config from the CLI skeleton. Use a config file intentionally.")

    trace = MultiAgentWorkflow(config).run_text_loop(args.text, steps=args.steps)
    if args.trace_jsonl:
        output_path = write_trace_jsonl(trace, args.trace_jsonl)
        print(f"Trace JSONL written: {output_path}")
    if args.json:
        records = trace_to_records(trace)
        print(json.dumps(records if args.steps > 1 else records[-1], ensure_ascii=False, indent=2))
    else:
        for result in trace.results:
            _print_human(result)
    return 0


def _print_human(result: Any) -> None:
    print(f"Step {result.step_index}:")
    print("Speech Input:")
    print(f"  backend: {result.speech_input.backend}")
    print(f"  transcript: {result.speech_input.transcript}")
    print(f"  wake_detected: {result.speech_input.wake_detected}")
    print("Intent:")
    print(f"  type: {result.intent.type.value}")
    print(f"  target: {result.intent.target}")
    print(f"  confidence: {result.intent.confidence}")
    print("Function Call:")
    print(f"  name: {result.function_call.name.value}")
    print(f"  arguments: {result.function_call.arguments}")
    print(f"  reason: {result.function_call.reason}")
    print("Vision:")
    print(f"  summary: {result.observation.summary}")
    print(f"  bbox_xywh: {result.observation.bbox_xywh}")
    print("Control:")
    print(f"  command: {result.command.name}")
    print(f"  dry_run: {result.command.dry_run}")
    print(f"  parameters: {result.command.parameters}")
    print("Execution:")
    print(f"  backend: {result.execution.backend}")
    print(f"  accepted: {result.execution.accepted}")
    print(f"  message: {result.execution.message}")
    print(f"  safety_status: {result.execution.safety_review.status.value}")
    print(f"  safety_violations: {result.execution.safety_review.violations}")
    print("Task State:")
    print(f"  status: {result.task_state.status.value}")
    print(f"  message: {result.task_state.message}")
    print("Response:")
    print(f"  {result.response}")
    print("Speech Output:")
    print(f"  backend: {result.speech_output.backend}")
    print(f"  audio_ref: {result.speech_output.audio_ref}")
    print(f"  played: {result.speech_output.played}")

if __name__ == "__main__":
    raise SystemExit(main())
