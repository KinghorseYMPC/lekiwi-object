from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class IntentType(str, Enum):
    CHAT = "chat"
    DESCRIBE_SCENE = "describe_scene"
    TRACK_TARGET = "track_target"
    TOUCH_TARGET = "touch_target"
    STOP = "stop"
    UNKNOWN = "unknown"


class FunctionName(str, Enum):
    NONE = "none"
    CHAT = "chat.respond"
    DESCRIBE_SCENE = "vision.describe_scene"
    TRACK_TARGET = "vision.track_target"
    TOUCH_TARGET = "manipulation.touch_target"
    STOP = "robot.stop"


class TaskStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass(frozen=True)
class Intent:
    type: IntentType
    target: str | None = None
    raw_text: str = ""
    confidence: float = 0.0


@dataclass(frozen=True)
class FunctionCall:
    name: FunctionName
    arguments: dict[str, Any] = field(default_factory=dict)
    reason: str = ""


@dataclass(frozen=True)
class VisionObservation:
    summary: str
    target: str | None = None
    bbox_xywh: tuple[int, int, int, int] | None = None
    confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ControlCommand:
    name: str
    parameters: dict[str, float | str | bool | None]
    dry_run: bool = True
    reason: str = ""


@dataclass(frozen=True)
class TaskState:
    name: FunctionName
    status: TaskStatus
    message: str
    target: str | None = None


@dataclass(frozen=True)
class WorkflowResult:
    intent: Intent
    function_call: FunctionCall
    observation: VisionObservation
    command: ControlCommand
    execution: Any
    task_state: TaskState
    response: str
    step_index: int = 0


@dataclass(frozen=True)
class WorkflowTrace:
    results: list[WorkflowResult]

    @property
    def final(self) -> WorkflowResult:
        if not self.results:
            raise ValueError("WorkflowTrace has no results.")
        return self.results[-1]
