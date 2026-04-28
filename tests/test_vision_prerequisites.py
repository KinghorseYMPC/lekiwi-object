from lekiwi_object.models import Intent, IntentType
from lekiwi_object.vision_backends import SampleFileVisionBackend
from lekiwi_object.vision_targets import VisionTargetRegistry


def test_target_registry_canonicalizes_aliases():
    registry = VisionTargetRegistry()
    assert registry.canonicalize("屏幕") == "电脑屏幕"
    assert registry.is_touchable("开关") is True
    assert registry.is_touchable("电脑屏幕") is False


def test_sample_file_backend_reads_explicit_scene_file():
    backend = SampleFileVisionBackend("samples/vision/desk_scene.json")
    observation = backend.observe(Intent(IntentType.TOUCH_TARGET, target="开关"))
    assert observation.target == "开关"
    assert observation.bbox_xywh == (420, 220, 50, 60)
    assert observation.metadata["opens_laptop_camera"] is False
    assert observation.metadata["camera_source"] == "sample_file"
