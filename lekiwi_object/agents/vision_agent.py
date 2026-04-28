from __future__ import annotations

from lekiwi_object.models import Intent, VisionObservation
from lekiwi_object.vision_backends import VisionBackend


class SimulatedVisionAgent:
    """Vision agent wrapper used by the multi-agent workflow."""

    def __init__(self, backend: VisionBackend):
        self.backend = backend

    def observe(self, intent: Intent) -> VisionObservation:
        return self.backend.observe(intent)
