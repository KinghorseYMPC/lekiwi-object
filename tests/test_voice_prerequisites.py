from lekiwi_object.voice_prerequisites import VoicePrerequisiteEvaluator


def test_default_voice_examples_are_covered():
    result = VoicePrerequisiteEvaluator().evaluate()
    assert result.accuracy == 1.0
    assert result.failures == ()
