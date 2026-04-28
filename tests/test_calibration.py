from lekiwi_object.calibration import (
    CalibrationGate,
    CalibrationStatus,
    CameraIntrinsics,
    HandEyeCalibration,
    uncalibrated_wrist_camera,
)


def test_missing_calibration_blocks_touch_geometry():
    report = CalibrationGate().evaluate(None)
    assert report.status == CalibrationStatus.MISSING
    assert "camera_intrinsics" in report.missing


def test_placeholder_calibration_is_incomplete():
    report = CalibrationGate().evaluate(uncalibrated_wrist_camera())
    assert report.status == CalibrationStatus.INCOMPLETE
    assert "camera_intrinsics" in report.missing


def test_complete_calibration_is_ready():
    calibration = HandEyeCalibration(
        camera_name="wrist_usb",
        intrinsics=CameraIntrinsics(fx=600.0, fy=601.0, cx=320.0, cy=240.0, distortion=(0.0, 0.0)),
        camera_to_end_effector=tuple(1.0 if idx in (0, 5, 10, 15) else 0.0 for idx in range(16)),
        reprojection_error_px=1.2,
    )
    report = CalibrationGate().evaluate(calibration)
    assert report.ready is True
