from __future__ import annotations

from dataclasses import dataclass

from lekiwi_object.config import SimulationConfig
from lekiwi_object.models import ControlCommand, Intent, IntentType, VisionObservation


@dataclass
class SimulatedTarget:
    name: str
    offset_x_norm: float
    offset_y_norm: float
    width_px: int
    height_px: int
    confidence: float = 0.75


class OfflineWorld:
    """Small deterministic world model for testing the workflow without SSH or hardware."""

    def __init__(self, config: SimulationConfig):
        self.config = config
        self.targets = {
            "电脑屏幕": SimulatedTarget("电脑屏幕", 0.32, -0.04, 150, 95, 0.78),
            "屏幕": SimulatedTarget("屏幕", 0.32, -0.04, 150, 95, 0.78),
            "开关": SimulatedTarget("开关", 0.16, 0.03, 55, 55, 0.7),
            "按钮": SimulatedTarget("按钮", -0.14, 0.08, 48, 48, 0.68),
            "人脸": SimulatedTarget("人脸", -0.25, -0.12, 90, 110, 0.73),
            "我": SimulatedTarget("我", -0.25, -0.12, 90, 110, 0.73),
            "目标": SimulatedTarget("目标", 0.22, 0.0, 80, 80, 0.62),
        }

    def observe(self, intent: Intent, default_target: str) -> VisionObservation:
        target_name = intent.target or default_target
        target = self._target_for(target_name, default_target)

        if intent.type == IntentType.DESCRIBE_SCENE:
            return VisionObservation(
                summary="模拟视觉：画面中有桌面、电脑屏幕、按钮和一个可触碰的开关区域。",
                target=target_name if target_name != "画面" else "画面",
                bbox_xywh=self._bbox(target),
                confidence=0.72,
                metadata={
                    "backend": "offline_world",
                    "visible_objects": ["电脑屏幕", "按钮", "开关"],
                },
            )

        if intent.type == IntentType.TRACK_TARGET:
            direction = _direction_text(target.offset_x_norm, target.offset_y_norm)
            return VisionObservation(
                summary=f"模拟视觉：检测到 {target.name}，目标{direction}。",
                target=target.name,
                bbox_xywh=self._bbox(target),
                confidence=target.confidence,
                metadata={
                    "backend": "offline_world",
                    "offset_x_norm": round(target.offset_x_norm, 4),
                    "offset_y_norm": round(target.offset_y_norm, 4),
                    "centered": abs(target.offset_x_norm) <= 0.05 and abs(target.offset_y_norm) <= 0.05,
                },
            )

        if intent.type == IntentType.TOUCH_TARGET:
            return VisionObservation(
                summary=f"模拟视觉：检测到 {target.name}，触碰前需要确认手眼标定和受保护运动。",
                target=target.name,
                bbox_xywh=self._bbox(target),
                confidence=target.confidence,
                metadata={
                    "backend": "offline_world",
                    "offset_x_norm": round(target.offset_x_norm, 4),
                    "offset_y_norm": round(target.offset_y_norm, 4),
                    "touch_calibrated": self.config.touch_calibrated,
                    "estimated_depth_m": 0.28,
                },
            )

        return VisionObservation(
            summary="模拟视觉：当前没有请求视觉动作。",
            target=target.name,
            confidence=0.0,
            metadata={"backend": "offline_world"},
        )

    def apply(self, command: ControlCommand) -> None:
        target_name = command.parameters.get("target")
        if not isinstance(target_name, str):
            return
        target = self.targets.get(target_name)
        if target is None:
            return

        if command.name == "center_target":
            theta = float(command.parameters.get("theta.vel", 0.0))
            correction = -theta * self.config.tracking_response_gain / 20.0
            target.offset_x_norm = _clamp(target.offset_x_norm - correction, -0.5, 0.5)

        if command.name == "hold_target":
            target.offset_x_norm *= 0.5
            target.offset_y_norm *= 0.5

    def _target_for(self, target_name: str, default_target: str) -> SimulatedTarget:
        if target_name in self.targets:
            return self.targets[target_name]
        if default_target in self.targets:
            return self.targets[default_target]
        return self.targets["目标"]

    def _bbox(self, target: SimulatedTarget) -> tuple[int, int, int, int]:
        center_x = int(self.config.image_width * (0.5 + target.offset_x_norm))
        center_y = int(self.config.image_height * (0.5 + target.offset_y_norm))
        x = center_x - target.width_px // 2
        y = center_y - target.height_px // 2
        return (x, y, target.width_px, target.height_px)


def _direction_text(offset_x: float, offset_y: float) -> str:
    if abs(offset_x) <= 0.05 and abs(offset_y) <= 0.05:
        return "已经接近画面中心"
    horizontal = "偏右" if offset_x > 0.05 else "偏左" if offset_x < -0.05 else "水平居中"
    vertical = "偏下" if offset_y > 0.05 else "偏上" if offset_y < -0.05 else "垂直居中"
    return f"{horizontal}、{vertical}"


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))
