from __future__ import annotations

from dataclasses import dataclass

from lekiwi_object.agents.voice_agent import TextVoiceAgent
from lekiwi_object.models import IntentType


@dataclass(frozen=True)
class VoiceCommandExample:
    text: str
    expected_intent: IntentType
    expected_target: str | None = None


@dataclass(frozen=True)
class VoiceEvaluationResult:
    total: int
    passed: int
    failures: tuple[str, ...]

    @property
    def accuracy(self) -> float:
        if self.total == 0:
            return 0.0
        return self.passed / self.total


DEFAULT_VOICE_EXAMPLES = (
    VoiceCommandExample("看一下桌面", IntentType.DESCRIBE_SCENE, "画面"),
    VoiceCommandExample("我正在电脑上做什么", IntentType.DESCRIBE_SCENE, "画面"),
    VoiceCommandExample("看我的电脑屏幕", IntentType.TRACK_TARGET, "电脑屏幕"),
    VoiceCommandExample("盯着屏幕", IntentType.TRACK_TARGET, "屏幕"),
    VoiceCommandExample("看着我", IntentType.TRACK_TARGET, "我"),
    VoiceCommandExample("碰一下那个开关", IntentType.TOUCH_TARGET, "开关"),
    VoiceCommandExample("按一下按钮", IntentType.TOUCH_TARGET, "按钮"),
    VoiceCommandExample("停下", IntentType.STOP, None),
    VoiceCommandExample("急停", IntentType.STOP, None),
)


class VoicePrerequisiteEvaluator:
    def __init__(self, agent: TextVoiceAgent | None = None):
        self.agent = agent or TextVoiceAgent()

    def evaluate(self, examples: tuple[VoiceCommandExample, ...] = DEFAULT_VOICE_EXAMPLES) -> VoiceEvaluationResult:
        failures: list[str] = []
        for example in examples:
            intent = self.agent.parse(example.text)
            if intent.type != example.expected_intent:
                failures.append(f"{example.text}: expected {example.expected_intent.value}, got {intent.type.value}")
                continue
            if example.expected_target is not None and intent.target != example.expected_target:
                failures.append(f"{example.text}: expected target {example.expected_target}, got {intent.target}")
        return VoiceEvaluationResult(total=len(examples), passed=len(examples) - len(failures), failures=tuple(failures))
