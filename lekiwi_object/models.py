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


@dataclass(frozen=True)
class Intent:
    type: IntentType
    target: str | None = None
    raw_text: str = ""
    confidence: float = 0.0


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
class WorkflowResult:
    intent: Intent
    observation: VisionObservation
    command: ControlCommand
    response: str

