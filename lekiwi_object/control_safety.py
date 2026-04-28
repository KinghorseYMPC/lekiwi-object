from __future__ import annotations

from lekiwi_object.config import SafetyConfig
from lekiwi_object.models import ControlCommand, SafetyReview, SafetyStatus


class ControlSafetyLayer:
    """Central safety checks for planned robot commands before any backend execution."""

    _LINEAR_KEYS = ("x.vel", "y.vel")
    _ANGULAR_KEYS = ("theta.vel",)

    def __init__(self, config: SafetyConfig):
        self.config = config

    def review(self, command: ControlCommand) -> SafetyReview:
        violations: list[str] = []

        if not command.dry_run and self.config.dry_run:
            violations.append("live command rejected while safety.dry_run is enabled")

        for key in self._LINEAR_KEYS:
            value = command.parameters.get(key)
            if value is not None and abs(float(value)) > self.config.max_linear_speed_mps:
                violations.append(f"{key} exceeds max_linear_speed_mps")

        for key in self._ANGULAR_KEYS:
            value = command.parameters.get(key)
            if value is not None and abs(float(value)) > self.config.max_angular_speed_dps:
                violations.append(f"{key} exceeds max_angular_speed_dps")

        duration = command.parameters.get("duration_s")
        if duration is not None and float(duration) > self.config.max_action_duration_s:
            violations.append("duration_s exceeds max_action_duration_s")

        if command.name == "guarded_touch" and command.dry_run is False:
            violations.append("live guarded_touch requires explicit hardware-stage approval")

        if command.name == "prepare_touch" and command.parameters.get("requires_calibration") is not True:
            violations.append("prepare_touch must require calibration")

        status = SafetyStatus.REJECTED if violations else SafetyStatus.ACCEPTED
        return SafetyReview(
            status=status,
            violations=tuple(violations),
            reviewed_command_name=command.name,
        )
