from __future__ import annotations

from lekiwi_object.models import FunctionCall, FunctionName, Intent, IntentType


class FunctionRouter:
    """Maps voice-agent intent into explicit workflow function calls."""

    def route(self, intent: Intent) -> FunctionCall:
        target = intent.target

        if intent.type == IntentType.DESCRIBE_SCENE:
            return FunctionCall(
                name=FunctionName.DESCRIBE_SCENE,
                arguments={"target": target or "画面"},
                reason="User asked for visual scene understanding.",
            )

        if intent.type == IntentType.TRACK_TARGET:
            return FunctionCall(
                name=FunctionName.TRACK_TARGET,
                arguments={"target": target or "目标", "goal": "keep_target_centered"},
                reason="User asked the robot arm/camera to follow a visual target.",
            )

        if intent.type == IntentType.TOUCH_TARGET:
            return FunctionCall(
                name=FunctionName.TOUCH_TARGET,
                arguments={"target": target or "目标", "requires_guarded_motion": True},
                reason="User asked for object interaction through touching.",
            )

        if intent.type == IntentType.STOP:
            return FunctionCall(
                name=FunctionName.STOP,
                arguments={"immediate": True},
                reason="User requested stop or emergency stop.",
            )

        if intent.type == IntentType.CHAT:
            return FunctionCall(
                name=FunctionName.CHAT,
                arguments={"text": intent.raw_text},
                reason="User asked for conversation instead of robot action.",
            )

        return FunctionCall(
            name=FunctionName.NONE,
            arguments={"text": intent.raw_text},
            reason="No reliable function call could be inferred.",
        )
