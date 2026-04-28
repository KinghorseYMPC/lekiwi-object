from lekiwi_object.config import load_config
from lekiwi_object.models import IntentType
from lekiwi_object.workflow import MultiAgentWorkflow


def test_describe_scene_intent():
    result = MultiAgentWorkflow(load_config()).run_text("看一下桌面")
    assert result.intent.type == IntentType.DESCRIBE_SCENE
    assert result.command.name == "no_motion"


def test_track_target_intent():
    result = MultiAgentWorkflow(load_config()).run_text("看我的电脑屏幕")
    assert result.intent.type == IntentType.TRACK_TARGET
    assert result.command.name == "center_target"


def test_touch_target_is_blocked_by_dry_run():
    result = MultiAgentWorkflow(load_config()).run_text("碰一下那个开关")
    assert result.intent.type == IntentType.TOUCH_TARGET
    assert result.command.name == "prepare_touch"
    assert result.command.dry_run is True
