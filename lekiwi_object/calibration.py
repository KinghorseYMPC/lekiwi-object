from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CalibrationStatus(str, Enum):
    READY = "ready"
    MISSING = "missing"
    INCOMPLETE = "incomplete"


@dataclass(frozen=True)
class CameraIntrinsics:
    fx: float | None = None
    fy: float | None = None
    cx: float | None = None
    cy: float | None = None
    distortion: tuple[float, ...] = ()

    @property
    def complete(self) -> bool:
        return all(value is not None and value > 0 for value in (self.fx, self.fy, self.cx, self.cy))


@dataclass(frozen=True)
class HandEyeCalibration:
    camera_name: str
    intrinsics: CameraIntrinsics | None = None
    camera_to_end_effector: tuple[float, ...] | None = None
    reprojection_error_px: float | None = None
    notes: str = ""


@dataclass(frozen=True)
class CalibrationReport:
    status: CalibrationStatus
    missing: tuple[str, ...]
    warnings: tuple[str, ...] = ()

    @property
    def ready(self) -> bool:
        return self.status == CalibrationStatus.READY


class CalibrationGate:
    """Checks whether vision-to-touch geometry is ready for hardware execution."""

    def __init__(self, max_reprojection_error_px: float = 3.0):
        self.max_reprojection_error_px = max_reprojection_error_px

    def evaluate(self, calibration: HandEyeCalibration | None) -> CalibrationReport:
        if calibration is None:
            return CalibrationReport(
                status=CalibrationStatus.MISSING,
                missing=("camera_intrinsics", "camera_to_end_effector", "reprojection_error_px"),
            )

        missing: list[str] = []
        warnings: list[str] = []
        if calibration.intrinsics is None or not calibration.intrinsics.complete:
            missing.append("camera_intrinsics")
        if calibration.camera_to_end_effector is None or len(calibration.camera_to_end_effector) != 16:
            missing.append("camera_to_end_effector")
        if calibration.reprojection_error_px is None:
            missing.append("reprojection_error_px")
        elif calibration.reprojection_error_px > self.max_reprojection_error_px:
            warnings.append("reprojection_error_px_above_threshold")

        if missing:
            return CalibrationReport(
                status=CalibrationStatus.INCOMPLETE,
                missing=tuple(missing),
                warnings=tuple(warnings),
            )
        if warnings:
            return CalibrationReport(status=CalibrationStatus.INCOMPLETE, missing=(), warnings=tuple(warnings))
        return CalibrationReport(status=CalibrationStatus.READY, missing=(), warnings=())


def uncalibrated_wrist_camera() -> HandEyeCalibration:
    return HandEyeCalibration(camera_name="wrist_usb", notes="Placeholder until real camera calibration is collected.")
