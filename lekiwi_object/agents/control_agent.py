from __future__ import annotations

from lekiwi_object.config import SafetyConfig
from lekiwi_object.models import ControlCommand, Intent, IntentType, VisionObservation
from lekiwi_object.touch_planning import TouchPlanner


class DryRunControlAgent:
    """Maps intents and observations to safe commands without moving hardware."""

    def __init__(self, safety: SafetyConfig):
        self.safety = safety
        self.touch_planner = TouchPlanner()

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
            if abs(offset_x) <= self.safety.tracking_deadband_norm:
                return ControlCommand(
                    name="hold_target",
                    parameters={
                        "target": observation.target,
                        "theta.vel": 0.0,
                        "duration_s": 0.0,
                    },
                    dry_run=self.safety.dry_run,
                    reason="Target is inside the tracking deadband.",
                )
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
            touch_plan = self.touch_planner.plan(observation)
            plan_metadata = {
                "touch_plan_status": touch_plan.status.value,
                "touch_prerequisites": ",".join(touch_plan.prerequisites),
            }
            if touch_plan.ready and bool(observation.metadata.get("touch_calibrated", False)):
                return ControlCommand(
                    name="guarded_touch",
                    parameters={
                        "target": observation.target,
                        "estimated_depth_m": touch_plan.estimated_depth_m,
                        "duration_s": self.safety.max_action_duration_s,
                        **plan_metadata,
                    },
                    dry_run=self.safety.dry_run,
                    reason="Touch plan is ready but remains dry-run unless live mode is intentionally enabled.",
                )
            return ControlCommand(
                name="prepare_touch",
                parameters={
                    "target": observation.target,
                    "requires_calibration": True,
                    "duration_s": 0.0,
                    **plan_metadata,
                },
                dry_run=True,
                reason=touch_plan.reason,
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
