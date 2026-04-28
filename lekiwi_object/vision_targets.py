from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VisionTargetSpec:
    name: str
    aliases: tuple[str, ...]
    touchable: bool = False
    trackable: bool = True


DEFAULT_TARGET_SPECS = (
    VisionTargetSpec("电脑屏幕", aliases=("屏幕", "电脑", "显示器"), touchable=False, trackable=True),
    VisionTargetSpec("开关", aliases=("那个开关", "开关按钮"), touchable=True, trackable=True),
    VisionTargetSpec("按钮", aliases=("按键", "那个按钮"), touchable=True, trackable=True),
    VisionTargetSpec("人脸", aliases=("我", "脸", "人"), touchable=False, trackable=True),
)


class VisionTargetRegistry:
    def __init__(self, specs: tuple[VisionTargetSpec, ...] = DEFAULT_TARGET_SPECS):
        self.specs = specs

    def canonicalize(self, name: str | None) -> str | None:
        if name is None:
            return None
        cleaned = name.strip()
        for spec in self.specs:
            if cleaned == spec.name or cleaned in spec.aliases:
                return spec.name
        return cleaned or None

    def is_touchable(self, name: str | None) -> bool:
        canonical = self.canonicalize(name)
        return any(spec.name == canonical and spec.touchable for spec in self.specs)

    def is_trackable(self, name: str | None) -> bool:
        canonical = self.canonicalize(name)
        return any(spec.name == canonical and spec.trackable for spec in self.specs)
