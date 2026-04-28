from lekiwi_object.config import SafetyConfig
from lekiwi_object.control_safety import ControlSafetyLayer
from lekiwi_object.models import ControlCommand, SafetyStatus


def test_safety_accepts_zero_stop_command():
    review = ControlSafetyLayer(SafetyConfig()).review(
        ControlCommand(name="stop", parameters={"x.vel": 0.0, "y.vel": 0.0, "theta.vel": 0.0})
    )
    assert review.status == SafetyStatus.ACCEPTED


def test_safety_rejects_long_duration():
    review = ControlSafetyLayer(SafetyConfig(max_action_duration_s=0.5)).review(
        ControlCommand(name="center_target", parameters={"duration_s": 2.0})
    )
    assert review.status == SafetyStatus.REJECTED
    assert "duration_s" in review.violations[0]


def test_safety_rejects_live_guarded_touch():
    review = ControlSafetyLayer(SafetyConfig(dry_run=False)).review(
        ControlCommand(name="guarded_touch", parameters={"duration_s": 0.1}, dry_run=False)
    )
    assert review.status == SafetyStatus.REJECTED
    assert "guarded_touch" in review.violations[0]
