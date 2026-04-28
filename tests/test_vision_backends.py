from lekiwi_object.agents.vision_agent import SimulatedVisionAgent
from lekiwi_object.config import load_config
from lekiwi_object.models import Intent, IntentType
from lekiwi_object.simulation import OfflineWorld
from lekiwi_object.vision_backends import OfflineVisionBackend


def test_offline_vision_backend_describes_scene():
    config = load_config()
    backend = OfflineVisionBackend(config.vision, OfflineWorld(config.simulation))
    observation = backend.observe(Intent(IntentType.DESCRIBE_SCENE, target="画面"))
    assert observation.target == "画面"
    assert "visible_objects" in observation.metadata
    assert observation.metadata["vision_backend"] == "offline_world"


def test_vision_agent_delegates_to_backend():
    config = load_config()
    backend = OfflineVisionBackend(config.vision, OfflineWorld(config.simulation))
    agent = SimulatedVisionAgent(backend)
    observation = agent.observe(Intent(IntentType.TRACK_TARGET, target="电脑屏幕"))
    assert observation.target == "电脑屏幕"
    assert "offset_x_norm" in observation.metadata
