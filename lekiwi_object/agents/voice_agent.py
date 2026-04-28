from __future__ import annotations

from difflib import SequenceMatcher

from lekiwi_object.models import Intent, IntentType


_INTENT_EXAMPLES: list[tuple[IntentType, str | None, tuple[str, ...]]] = [
    (IntentType.STOP, "停止", ("停", "停止", "别动", "急停", "stop")),
    (IntentType.DESCRIBE_SCENE, "画面", ("看一下", "看到了什么", "识别", "做什么", "描述", "场景", "画面", "桌面")),
    (IntentType.TRACK_TARGET, "目标", ("跟随", "看着", "盯着", "盯", "追踪", "转向", "屏幕", "人脸")),
    (IntentType.TOUCH_TARGET, "目标", ("碰", "触碰", "点一下", "按一下", "开关", "按钮")),
    (IntentType.CHAT, None, ("你好", "介绍", "聊天", "你是谁")),
]


_TARGET_HINTS = (
    "电脑屏幕",
    "屏幕",
    "开关",
    "按钮",
    "人脸",
    "我",
    "杯子",
    "目标",
)


class TextVoiceAgent:
    """Text-mode stand-in for the future speech agent."""

    def parse(self, text: str) -> Intent:
        cleaned = text.strip()
        if not cleaned:
            return Intent(IntentType.UNKNOWN, raw_text=text, confidence=0.0)

        best_type = IntentType.UNKNOWN
        best_score = 0.0
        for intent_type, _fallback_target, keywords in _INTENT_EXAMPLES:
            keyword_score = max((_score(cleaned, keyword) for keyword in keywords), default=0.0)
            if keyword_score > best_score:
                best_score = keyword_score
                best_type = intent_type

        if best_score < 0.35:
            best_type = IntentType.CHAT

        target = _extract_target(cleaned)
        if best_type == IntentType.DESCRIBE_SCENE and target is None:
            target = "画面"
        elif best_type in {IntentType.TRACK_TARGET, IntentType.TOUCH_TARGET} and target is None:
            target = "目标"

        return Intent(best_type, target=target, raw_text=text, confidence=round(best_score, 3))

    def render_response(self, intent: Intent, action_text: str) -> str:
        if intent.type == IntentType.UNKNOWN:
            return "我还没有听懂这条指令，可以换一种说法。"
        if intent.type == IntentType.CHAT:
            return "我在，当前可以先用文本方式调试语音、视觉和控制闭环。"
        return action_text


def _score(text: str, keyword: str) -> float:
    if keyword in text:
        return 1.0
    if len(keyword) <= 3:
        return 0.0
    return SequenceMatcher(None, text, keyword).ratio()


def _extract_target(text: str) -> str | None:
    if "正在电脑" in text:
        return None
    for hint in _TARGET_HINTS:
        if hint in text:
            return hint
    if "那个" in text:
        return text.split("那个", 1)[1].strip() or "目标"
    if "这个" in text:
        return text.split("这个", 1)[1].strip() or "目标"
    return None
