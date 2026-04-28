from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from lekiwi_object.camera_sources import CameraSource, CameraSourcePolicy
from lekiwi_object.config import PROJECT_ROOT, VisionConfig
from lekiwi_object.models import Intent, IntentType, VisionObservation
from lekiwi_object.simulation import OfflineWorld
from lekiwi_object.vision_targets import VisionTargetRegistry


class VisionBackend(Protocol):
    """Backend contract for scene understanding, detection, and localization."""

    @property
    def name(self) -> str:
        """Human-readable backend name for logs and trace output."""

    def observe(self, intent: Intent) -> VisionObservation:
        """Return a vision observation for the current task intent."""


class OfflineVisionBackend:
    """Vision backend backed by the local deterministic simulation world."""

    name = "offline_world"

    def __init__(self, config: VisionConfig, world: OfflineWorld, camera_source: CameraSource | None = None):
        self.config = config
        self.world = world
        self.camera_source = camera_source or CameraSourcePolicy().resolve(config)

    def observe(self, intent: Intent) -> VisionObservation:
        observation = self.world.observe(intent, self.config.default_target)
        metadata = {
            **observation.metadata,
            "vision_backend": self.name,
            "camera_source": self.camera_source.kind.value,
            "opens_laptop_camera": self.camera_source.opens_local_camera,
        }
        return VisionObservation(
            summary=observation.summary,
            target=observation.target,
            bbox_xywh=observation.bbox_xywh,
            confidence=observation.confidence,
            metadata=metadata,
        )


class SampleFileVisionBackend:
    """Vision backend for explicit sample JSON files, never a live camera."""

    name = "sample_file"

    def __init__(self, path: str | Path, target_registry: VisionTargetRegistry | None = None):
        self.path = _resolve_project_path(path)
        self.target_registry = target_registry or VisionTargetRegistry()
        self._data = json.loads(self.path.read_text(encoding="utf-8"))

    def observe(self, intent: Intent) -> VisionObservation:
        requested = self.target_registry.canonicalize(intent.target)
        objects = self._data.get("objects", [])
        selected = _select_object(objects, requested)
        visible_names = [obj.get("name", "unknown") for obj in objects]

        if intent.type == IntentType.DESCRIBE_SCENE:
            summary = self._data.get("summary") or f"样例视觉：画面中有 {', '.join(visible_names)}。"
        elif selected is not None:
            summary = f"样例视觉：检测到 {selected.get('name')}。"
        else:
            summary = f"样例视觉：没有找到 {requested or '目标'}。"

        bbox = tuple(selected.get("bbox_xywh", ())) if selected is not None else None
        if bbox is not None and len(bbox) != 4:
            bbox = None
        metadata = {
            "vision_backend": self.name,
            "camera_source": "sample_file",
            "opens_laptop_camera": False,
            "sample_path": str(self.path.relative_to(PROJECT_ROOT)),
            "visible_objects": visible_names,
        }
        if selected is not None:
            metadata.update(selected.get("metadata", {}))

        return VisionObservation(
            summary=summary,
            target=selected.get("name") if selected is not None else requested,
            bbox_xywh=bbox,
            confidence=float(selected.get("confidence", 0.0)) if selected is not None else 0.0,
            metadata=metadata,
        )


def _select_object(objects: list[dict], requested: str | None) -> dict | None:
    if not objects:
        return None
    if requested is None or requested == "画面":
        return objects[0]
    registry = VisionTargetRegistry()
    for obj in objects:
        if registry.canonicalize(obj.get("name")) == requested:
            return obj
    return None


def _resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    resolved = candidate.resolve()
    project_root = PROJECT_ROOT.resolve()
    if resolved != project_root and project_root not in resolved.parents:
        raise ValueError("Sample vision file must stay inside the lekiwi object project folder.")
    return resolved
