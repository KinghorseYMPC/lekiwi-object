from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from lekiwi_object.config import PROJECT_ROOT
from lekiwi_object.models import WorkflowResult, WorkflowTrace


def result_to_record(result: WorkflowResult) -> dict[str, Any]:
    """Convert one workflow step into a JSON-safe trace record."""

    return _to_jsonable(result)


def trace_to_records(trace: WorkflowTrace) -> list[dict[str, Any]]:
    return [result_to_record(result) for result in trace.results]


def write_trace_jsonl(trace: WorkflowTrace, path: str | Path) -> Path:
    """Write workflow trace records as JSONL under the project directory."""

    output_path = _resolve_project_path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in trace_to_records(trace):
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
            handle.write("\n")
    return output_path


def _resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    resolved = candidate.resolve()
    project_root = PROJECT_ROOT.resolve()
    if resolved != project_root and project_root not in resolved.parents:
        raise ValueError("Trace export path must stay inside the lekiwi object project folder.")
    return resolved


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: _to_jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(item) for item in value]
    return value
