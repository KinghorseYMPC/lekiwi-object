from lekiwi_object.config import VoiceConfig, load_config
from lekiwi_object.speech_io import MockSpeechIO
from lekiwi_object.workflow import MultiAgentWorkflow


def test_mock_speech_io_transcribes_text_input():
    speech = MockSpeechIO(VoiceConfig())
    result = speech.listen_text("看一下桌面")
    assert result.transcript == "看一下桌面"
    assert result.backend == "mock_asr"
    assert result.wake_detected is True


def test_mock_speech_io_strips_wake_word():
    speech = MockSpeechIO(VoiceConfig(require_wake_word=True))
    result = speech.listen_text("小车，看一下桌面")
    assert result.transcript == "看一下桌面"
    assert result.wake_detected is True


def test_mock_speech_io_blocks_when_wake_word_required_but_missing():
    speech = MockSpeechIO(VoiceConfig(require_wake_word=True))
    result = speech.listen_text("看一下桌面")
    assert result.transcript == ""
    assert result.confidence == 0.0
    assert result.wake_detected is False


def test_workflow_records_speech_input_and_output():
    result = MultiAgentWorkflow(load_config()).run_text("看一下桌面")
    assert result.speech_input.transcript == "看一下桌面"
    assert result.speech_output.backend == "mock_tts"
    assert result.speech_output.text == result.response
