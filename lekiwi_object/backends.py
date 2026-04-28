from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from lekiwi_object.models import ControlCommand


@dataclass(frozen=True)
class CommandExecution:
    accepted: bool
    backend: str
    message: str
    command_name: str


class RobotBackend(Protocol):
    def execute(self, command: ControlCommand) -> CommandExecution:
        """Execute or simulate a command."""


@dataclass
class DryRunRobotBackend:
    """Laptop-only backend that records commands and never contacts the Raspberry Pi."""

    history: list[ControlCommand] = field(default_factory=list)

    def execute(self, command: ControlCommand) -> CommandExecution:
        self.history.append(command)
        if command.dry_run:
            return CommandExecution(
                accepted=True,
                backend="dry_run",
                message="Command recorded locally; no SSH or robot motion was attempted.",
                command_name=command.name,
            )

        return CommandExecution(
            accepted=False,
            backend="dry_run",
            message="Live command rejected by the offline dry-run backend.",
            command_name=command.name,
        )
