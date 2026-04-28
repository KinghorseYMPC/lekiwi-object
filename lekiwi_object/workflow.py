from __future__ import annotations

from lekiwi_object.agents.control_agent import DryRunControlAgent
from lekiwi_object.agents.vision_agent import SimulatedVisionAgent
from lekiwi_object.agents.voice_agent import TextVoiceAgent
from lekiwi_object.config import AppConfig
from lekiwi_object.models import IntentType, WorkflowResult


class MultiAgentWorkflow:
    def __init__(self, config: AppConfig):
        self.config = config
        self.voice = TextVoiceAgent()
        self.vision = SimulatedVisionAgent(config.vision)
        self.control = DryRunControlAgent(config.safety)

    def run_text(self, text: str) -> WorkflowResult:
        intent = self.voice.parse(text)
        observation = self.vision.observe(intent)
        command = self.control.plan(intent, observation)
        response = self.voice.render_response(intent, _response_for(intent.type, observation.summary, command.name))
        return WorkflowResult(intent=intent, observation=observation, command=command, response=response)


def _response_for(intent_type: IntentType, vision_summary: str, command_name: str) -> str:
    if intent_type == IntentType.DESCRIBE_SCENE:
        return vision_summary
    if intent_type == IntentType.TRACK_TARGET:
        return f"{vision_summary} 我会生成 {command_name} 指令让目标回到画面中心。"
    if intent_type == IntentType.TOUCH_TARGET:
        return f"{vision_summary} 目前先停在安全 dry-run，下一阶段接入标定和受保护动作。"
    if intent_type == IntentType.STOP:
        return "已生成停止指令。"
    return "收到。"

