import pytest

from lekiwi_object.camera_sources import CameraSourceKind, CameraSourcePolicy
from lekiwi_object.config import VisionConfig


def test_default_camera_source_is_offline_and_private():
    source = CameraSourcePolicy().resolve(VisionConfig())
    assert source.kind == CameraSourceKind.OFFLINE_WORLD
    assert source.opens_local_camera is False


def test_raspberry_pi_usb_camera_source_is_allowed():
    source = CameraSourcePolicy().resolve(VisionConfig(source="raspberry_pi_usb"))
    assert source.kind == CameraSourceKind.RASPBERRY_PI_USB
    assert source.opens_local_camera is False


def test_laptop_camera_source_is_forbidden():
    with pytest.raises(ValueError, match="Laptop camera"):
        CameraSourcePolicy().resolve(VisionConfig(source="laptop_camera"))


def test_laptop_camera_flag_is_forbidden():
    with pytest.raises(ValueError, match="Laptop camera"):
        CameraSourcePolicy().resolve(VisionConfig(allow_laptop_camera=True))
