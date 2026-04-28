from __future__ import annotations

from typing import Protocol

from lekiwi_object.camera_sources import CameraSource, CameraSourcePolicy
from lekiwi_object.config import VisionConfig
from lekiwi_object.models import Intent, VisionObservation
from lekiwi_object.simulation import OfflineWorld


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
