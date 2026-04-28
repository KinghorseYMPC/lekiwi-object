from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from lekiwi_object.calibration import CalibrationGate, HandEyeCalibration
from lekiwi_object.models import VisionObservation
from lekiwi_object.vision_targets import VisionTargetRegistry


class TouchPlanStatus(str, Enum):
    READY_DRY_RUN = "ready_dry_run"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class TouchPlan:
    status: TouchPlanStatus
    target: str | None
    reason: str
    bbox_xywh: tuple[int, int, int, int] | None = None
    estimated_depth_m: float | None = None
    prerequisites: tuple[str, ...] = ()

    @property
    def ready(self) -> bool:
        return self.status == TouchPlanStatus.READY_DRY_RUN


class TouchPlanner:
    """Builds a dry-run touch plan and lists unmet hardware prerequisites."""

    def __init__(
        self,
        calibration: HandEyeCalibration | None = None,
        target_registry: VisionTargetRegistry | None = None,
    ):
        self.calibration = calibration
        self.target_registry = target_registry or VisionTargetRegistry()
        self.calibration_gate = CalibrationGate()

    def plan(self, observation: VisionObservation) -> TouchPlan:
        target = self.target_registry.canonicalize(observation.target)
        prerequisites: list[str] = []

        if target is None:
            prerequisites.append("target_detected")
        elif not self.target_registry.is_touchable(target):
            prerequisites.append("target_must_be_touchable")

        if observation.bbox_xywh is None:
            prerequisites.append("target_bbox")

        depth = observation.metadata.get("estimated_depth_m")
        if depth is None:
            prerequisites.append("estimated_depth_m")
        else:
            depth = float(depth)

        calibration_report = self.calibration_gate.evaluate(self.calibration)
        if not calibration_report.ready:
            prerequisites.extend(f"calibration:{item}" for item in calibration_report.missing)
            prerequisites.extend(f"calibration:{item}" for item in calibration_report.warnings)

        if prerequisites:
            return TouchPlan(
                status=TouchPlanStatus.BLOCKED,
                target=target,
                bbox_xywh=observation.bbox_xywh,
                estimated_depth_m=depth if isinstance(depth, float) else None,
                prerequisites=tuple(dict.fromkeys(prerequisites)),
                reason="Touch plan blocked until prerequisites are satisfied.",
            )

        return TouchPlan(
            status=TouchPlanStatus.READY_DRY_RUN,
            target=target,
            bbox_xywh=observation.bbox_xywh,
            estimated_depth_m=depth if isinstance(depth, float) else None,
            reason="Touch plan is geometrically ready for dry-run review only.",
        )
