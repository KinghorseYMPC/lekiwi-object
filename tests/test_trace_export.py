import json

import pytest

from lekiwi_object.config import PROJECT_ROOT, load_config
from lekiwi_object.trace_export import trace_to_records, write_trace_jsonl
from lekiwi_object.workflow import MultiAgentWorkflow


def test_trace_to_records_contains_complete_agent_chain():
    trace = MultiAgentWorkflow(load_config()).run_text_loop("看一下桌面", steps=1)
    record = trace_to_records(trace)[0]
    assert record["speech_input"]["backend"] == "mock_asr"
    assert record["function_call"]["name"] == "vision.describe_scene"
    assert record["observation"]["metadata"]["opens_laptop_camera"] is False
    assert record["execution"]["safety_review"]["status"] == "accepted"
    assert record["speech_output"]["backend"] == "mock_tts"


def test_write_trace_jsonl_under_project_folder():
    trace = MultiAgentWorkflow(load_config()).run_text_loop("看我的电脑屏幕", steps=2)
    output_path = write_trace_jsonl(trace, PROJECT_ROOT / "logs" / "test_trace.jsonl")
    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["step_index"] == 0


def test_write_trace_jsonl_rejects_outside_project():
    trace = MultiAgentWorkflow(load_config()).run_text_loop("看一下桌面", steps=1)
    with pytest.raises(ValueError, match="project folder"):
        write_trace_jsonl(trace, PROJECT_ROOT.parent / "outside_trace.jsonl")
