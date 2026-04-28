from lekiwi_object.calibration import CameraIntrinsics, HandEyeCalibration
from lekiwi_object.models import VisionObservation
from lekiwi_object.touch_planning import TouchPlanner, TouchPlanStatus


def test_touch_plan_blocks_without_calibration():
    observation = VisionObservation(
        summary="detected switch",
        target="开关",
        bbox_xywh=(10, 20, 30, 40),
        confidence=0.8,
        metadata={"estimated_depth_m": 0.3},
    )
    plan = TouchPlanner().plan(observation)
    assert plan.status == TouchPlanStatus.BLOCKED
    assert any(item.startswith("calibration:") for item in plan.prerequisites)


def test_touch_plan_blocks_non_touchable_target():
    observation = VisionObservation(
        summary="detected screen",
        target="电脑屏幕",
        bbox_xywh=(10, 20, 30, 40),
        confidence=0.8,
        metadata={"estimated_depth_m": 0.3},
    )
    plan = TouchPlanner().plan(observation)
    assert "target_must_be_touchable" in plan.prerequisites


def test_touch_plan_ready_with_complete_prerequisites():
    calibration = HandEyeCalibration(
        camera_name="wrist_usb",
        intrinsics=CameraIntrinsics(fx=600.0, fy=600.0, cx=320.0, cy=240.0),
        camera_to_end_effector=tuple(1.0 if idx in (0, 5, 10, 15) else 0.0 for idx in range(16)),
        reprojection_error_px=1.0,
    )
    observation = VisionObservation(
        summary="detected switch",
        target="开关",
        bbox_xywh=(10, 20, 30, 40),
        confidence=0.8,
        metadata={"estimated_depth_m": 0.3},
    )
    plan = TouchPlanner(calibration=calibration).plan(observation)
    assert plan.ready is True
    assert plan.status == TouchPlanStatus.READY_DRY_RUN
