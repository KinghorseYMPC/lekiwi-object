from lekiwi_object.config import load_config
from lekiwi_object.function_calling import FunctionRouter
from lekiwi_object.models import FunctionName, Intent, IntentType, TaskStatus
from lekiwi_object.workflow import MultiAgentWorkflow


def test_router_maps_scene_request_to_vision_function():
    call = FunctionRouter().route(Intent(IntentType.DESCRIBE_SCENE, target="画面", raw_text="看一下桌面"))
    assert call.name == FunctionName.DESCRIBE_SCENE
    assert call.arguments["target"] == "画面"


def test_router_maps_touch_request_to_manipulation_function():
    call = FunctionRouter().route(Intent(IntentType.TOUCH_TARGET, target="开关", raw_text="碰一下那个开关"))
    assert call.name == FunctionName.TOUCH_TARGET
    assert call.arguments["requires_guarded_motion"] is True


def test_scene_workflow_completes_function_call():
    result = MultiAgentWorkflow(load_config()).run_text("看一下桌面")
    assert result.function_call.name == FunctionName.DESCRIBE_SCENE
    assert result.task_state.status == TaskStatus.COMPLETED


def test_touch_workflow_is_blocked_without_calibration():
    result = MultiAgentWorkflow(load_config()).run_text("碰一下那个开关")
    assert result.function_call.name == FunctionName.TOUCH_TARGET
    assert result.task_state.status == TaskStatus.BLOCKED


def test_tracking_workflow_status_moves_from_running_to_completed():
    trace = MultiAgentWorkflow(load_config()).run_text_loop("看我的电脑屏幕", steps=20)
    assert trace.results[0].task_state.status == TaskStatus.RUNNING
    assert trace.final.function_call.name == FunctionName.TRACK_TARGET
    assert trace.final.task_state.status == TaskStatus.COMPLETED
