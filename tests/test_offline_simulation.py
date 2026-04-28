from lekiwi_object.config import load_config
from lekiwi_object.models import IntentType
from lekiwi_object.workflow import MultiAgentWorkflow


def test_tracking_loop_reduces_horizontal_offset():
    trace = MultiAgentWorkflow(load_config()).run_text_loop("看我的电脑屏幕", steps=4)
    offsets = [abs(result.observation.metadata["offset_x_norm"]) for result in trace.results]
    assert trace.final.intent.type == IntentType.TRACK_TARGET
    assert offsets[-1] < offsets[0]


def test_tracking_loop_eventually_holds_when_centered():
    trace = MultiAgentWorkflow(load_config()).run_text_loop("看我的电脑屏幕", steps=20)
    assert trace.final.command.name == "hold_target"


def test_stop_command_is_zero_velocity():
    result = MultiAgentWorkflow(load_config()).run_text("停下")
    assert result.intent.type == IntentType.STOP
    assert result.command.name == "stop"
    assert result.command.parameters["x.vel"] == 0.0
    assert result.command.parameters["theta.vel"] == 0.0
