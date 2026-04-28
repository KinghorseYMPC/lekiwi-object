from __future__ import annotations

from typing import Protocol

from lekiwi_object.config import VoiceConfig
from lekiwi_object.models import SpeechInput, SpeechOutput


class SpeechIO(Protocol):
    def listen_text(self, text: str) -> SpeechInput:
        """Convert local text into a speech-recognition result."""

    def speak(self, text: str) -> SpeechOutput:
        """Convert response text into a speech-synthesis result."""


class MockSpeechIO:
    """Offline ASR/TTS stand-in that never opens a microphone or speaker."""

    def __init__(self, config: VoiceConfig):
        self.config = config
        self.spoken_history: list[SpeechOutput] = []

    def listen_text(self, text: str) -> SpeechInput:
        raw = text.strip()
        transcript, wake_detected = self._strip_wake_word(raw)
        if self.config.require_wake_word and not wake_detected:
            transcript = ""

        return SpeechInput(
            transcript=transcript,
            backend=self.config.asr_backend,
            confidence=1.0 if transcript else 0.0,
            wake_detected=wake_detected,
            raw_input=raw,
        )

    def speak(self, text: str) -> SpeechOutput:
        output = SpeechOutput(
            text=text,
            backend=self.config.tts_backend,
            audio_ref="mock://tts/latest",
            played=False,
        )
        self.spoken_history.append(output)
        return output

    def _strip_wake_word(self, text: str) -> tuple[str, bool]:
        lowered = text.lower()
        for wake_word in self.config.wake_words:
            wake = wake_word.lower()
            if lowered.startswith(wake):
                return text[len(wake_word) :].lstrip(" ，,。"), True
        return text, not self.config.require_wake_word
