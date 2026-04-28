from __future__ import annotations

from lekiwi_object.config import SafetyConfig
from lekiwi_object.models import ControlCommand, Intent, IntentType, VisionObservation


class DryRunControlAgent:
    """Maps intents and observations to safe commands without moving hardware."""

    def __init__(self, safety: SafetyConfig):
        self.safety = safety

    def plan(self, intent: Intent, observation: VisionObservation) -> ControlCommand:
        if intent.type == IntentType.STOP:
            return ControlCommand(
                name="stop",
                parameters={"x.vel": 0.0, "y.vel": 0.0, "theta.vel": 0.0},
                dry_run=self.safety.dry_run,
                reason="Stop requested.",
            )

        if intent.type == IntentType.TRACK_TARGET:
            offset_x = float(observation.metadata.get("offset_x_norm", 0.0))
            theta = _clip(-offset_x * self.safety.max_angular_speed_dps, self.safety.max_angular_speed_dps)
            return ControlCommand(
                name="center_target",
                parameters={
                    "target": observation.target,
                    "theta.vel": round(theta, 3),
                    "duration_s": self.safety.max_action_duration_s,
                },
                dry_run=self.safety.dry_run,
                reason="Center target in wrist camera view.",
            )

        if intent.type == IntentType.TOUCH_TARGET:
            return ControlCommand(
                name="prepare_touch",
                parameters={
                    "target": observation.target,
                    "requires_calibration": True,
                    "duration_s": 0.0,
                },
                dry_run=True,
                reason="Touch is blocked until calibration and guarded motion are implemented.",
            )

        if intent.type == IntentType.DESCRIBE_SCENE:
            return ControlCommand(
                name="no_motion",
                parameters={"target": observation.target},
                dry_run=True,
                reason="Scene description does not require motion.",
            )

        return ControlCommand(
            name="no_motion",
            parameters={},
            dry_run=True,
            reason="No actionable robot command.",
        )


def _clip(value: float, limit: float) -> float:
    return max(-limit, min(limit, value))

