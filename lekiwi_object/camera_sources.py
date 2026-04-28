from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from lekiwi_object.config import VisionConfig


class CameraSourceKind(str, Enum):
    OFFLINE_WORLD = "offline_world"
    SAMPLE_FILE = "sample_file"
    RASPBERRY_PI_USB = "raspberry_pi_usb"


@dataclass(frozen=True)
class CameraSource:
    kind: CameraSourceKind
    description: str
    privacy_note: str
    opens_local_camera: bool = False


class CameraSourcePolicy:
    """Enforces the project rule that laptop cameras must never be used."""

    _ALLOWED = {
        CameraSourceKind.OFFLINE_WORLD.value: CameraSource(
            kind=CameraSourceKind.OFFLINE_WORLD,
            description="Deterministic offline simulated camera observations.",
            privacy_note="No physical camera is opened.",
            opens_local_camera=False,
        ),
        CameraSourceKind.SAMPLE_FILE.value: CameraSource(
            kind=CameraSourceKind.SAMPLE_FILE,
            description="Pre-recorded local sample image or metadata file.",
            privacy_note="Reads an explicit file only; does not open any camera.",
            opens_local_camera=False,
        ),
        CameraSourceKind.RASPBERRY_PI_USB.value: CameraSource(
            kind=CameraSourceKind.RASPBERRY_PI_USB,
            description="USB camera directly connected to the Raspberry Pi.",
            privacy_note="The camera is on the robot side; laptop camera remains forbidden.",
            opens_local_camera=False,
        ),
    }

    _FORBIDDEN = {"laptop_camera", "local_camera", "webcam", "opencv_index", "cv2_video_capture"}

    def resolve(self, config: VisionConfig) -> CameraSource:
        source = config.source.strip().lower()
        if config.allow_laptop_camera or source in self._FORBIDDEN:
            raise ValueError("Laptop camera use is forbidden by project policy.")
        if source not in self._ALLOWED:
            allowed = ", ".join(sorted(self._ALLOWED))
            raise ValueError(f"Unsupported camera source '{config.source}'. Allowed sources: {allowed}.")
        return self._ALLOWED[source]
