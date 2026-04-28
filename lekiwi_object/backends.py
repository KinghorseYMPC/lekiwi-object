from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from lekiwi_object.config import SafetyConfig
from lekiwi_object.control_safety import ControlSafetyLayer
from lekiwi_object.models import ControlCommand, SafetyReview, SafetyStatus


@dataclass(frozen=True)
class CommandExecution:
    accepted: bool
    backend: str
    message: str
    command_name: str
    safety_review: SafetyReview


class RobotBackend(Protocol):
    def execute(self, command: ControlCommand) -> CommandExecution:
        """Execute or simulate a command."""


@dataclass
class DryRunRobotBackend:
    """Laptop-only backend that records commands and never contacts the Raspberry Pi."""

    history: list[ControlCommand] = field(default_factory=list)
    safety: ControlSafetyLayer = field(default_factory=lambda: ControlSafetyLayer(SafetyConfig()))

    def execute(self, command: ControlCommand) -> CommandExecution:
        safety_review = self.safety.review(command)
        self.history.append(command)
        if not safety_review.accepted:
            return CommandExecution(
                accepted=False,
                backend="dry_run",
                message="Command rejected by safety layer before any SSH or robot motion.",
                command_name=command.name,
                safety_review=safety_review,
            )

        if command.dry_run:
            return CommandExecution(
                accepted=True,
                backend="dry_run",
                message="Command recorded locally; no SSH or robot motion was attempted.",
                command_name=command.name,
                safety_review=safety_review,
            )

        return CommandExecution(
            accepted=False,
            backend="dry_run",
            message="Live command rejected by the offline dry-run backend.",
            command_name=command.name,
            safety_review=SafetyReview(
                status=SafetyStatus.REJECTED,
                violations=("offline dry-run backend cannot execute live commands",),
                reviewed_command_name=command.name,
            ),
        )
