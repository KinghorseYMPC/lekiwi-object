from __future__ import annotations

from lekiwi_object.config import VisionConfig
from lekiwi_object.simulation import OfflineWorld
from lekiwi_object.models import Intent, IntentType, VisionObservation


class SimulatedVisionAgent:
    """A deterministic vision backend for laptop-only workflow testing."""

    def __init__(self, config: VisionConfig, world: OfflineWorld | None = None):
        self.config = config
        self.world = world

    def observe(self, intent: Intent) -> VisionObservation:
        if self.world is not None:
            return self.world.observe(intent, self.config.default_target)

        target = intent.target or self.config.default_target

        if intent.type == IntentType.DESCRIBE_SCENE:
            return VisionObservation(
                summary="模拟视觉：画面中有桌面、电脑屏幕和一个可触碰的开关区域。",
                target=target,
                bbox_xywh=(220, 120, 180, 120),
                confidence=0.7,
                metadata={"backend": self.config.backend},
            )

        if intent.type == IntentType.TRACK_TARGET:
            return VisionObservation(
                summary=f"模拟视觉：检测到 {target}，目标略偏向画面右侧。",
                target=target,
                bbox_xywh=(360, 150, 120, 100),
                confidence=0.72,
                metadata={"offset_x_norm": 0.18, "offset_y_norm": -0.04},
            )

        if intent.type == IntentType.TOUCH_TARGET:
            return VisionObservation(
                summary=f"模拟视觉：检测到 {target}，需要先做深度/手眼标定后才能真实触碰。",
                target=target,
                bbox_xywh=(300, 180, 70, 70),
                confidence=0.65,
                metadata={"requires_calibration": True},
            )

        return VisionObservation(
            summary="模拟视觉：当前没有请求视觉动作。",
            target=target,
            confidence=0.0,
            metadata={"backend": self.config.backend},
        )
