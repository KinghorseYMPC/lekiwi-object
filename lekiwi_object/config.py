from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "default.json"


@dataclass(frozen=True)
class RobotConfig:
    host: str = "rasberrypi16.local"
    user: str = "gjy"
    zmq_command_port: int = 5555
    zmq_observation_port: int = 5556


@dataclass(frozen=True)
class SafetyConfig:
    dry_run: bool = True
    max_linear_speed_mps: float = 0.1
    max_angular_speed_dps: float = 20.0
    max_action_duration_s: float = 0.5
    tracking_deadband_norm: float = 0.05


@dataclass(frozen=True)
class VisionConfig:
    backend: str = "simulated"
    default_target: str = "电脑屏幕"
    source: str = "offline_world"
    allow_laptop_camera: bool = False
    raspberry_pi_camera_name: str = "wrist_usb"


@dataclass(frozen=True)
class VoiceConfig:
    backend: str = "text"
    asr_backend: str = "mock_asr"
    tts_backend: str = "mock_tts"
    require_wake_word: bool = False
    wake_words: tuple[str, ...] = ("lekiwi", "小车", "机器人")


@dataclass(frozen=True)
class SimulationConfig:
    image_width: int = 640
    image_height: int = 480
    tracking_response_gain: float = 0.12
    touch_calibrated: bool = False


@dataclass(frozen=True)
class AppConfig:
    robot: RobotConfig = RobotConfig()
    safety: SafetyConfig = SafetyConfig()
    vision: VisionConfig = VisionConfig()
    voice: VoiceConfig = VoiceConfig()
    simulation: SimulationConfig = SimulationConfig()


def _section(data: dict[str, Any], name: str) -> dict[str, Any]:
    value = data.get(name, {})
    if not isinstance(value, dict):
        raise ValueError(f"Config section '{name}' must be an object.")
    return value


def load_config(path: str | Path | None = None) -> AppConfig:
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    data = json.loads(config_path.read_text(encoding="utf-8"))
    config = AppConfig(
        robot=RobotConfig(**_section(data, "robot")),
        safety=SafetyConfig(**_section(data, "safety")),
        vision=VisionConfig(**_section(data, "vision")),
        voice=VoiceConfig(**_section(data, "voice")),
        simulation=SimulationConfig(**_section(data, "simulation")),
    )
    _validate_config(config)
    return config


def _validate_config(config: AppConfig) -> None:
    if config.vision.allow_laptop_camera:
        raise ValueError("Laptop camera use is forbidden by project policy.")
    if config.vision.source == "laptop_camera":
        raise ValueError("vision.source='laptop_camera' is forbidden by project policy.")
