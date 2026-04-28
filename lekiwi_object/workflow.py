from __future__ import annotations

from lekiwi_object.agents.control_agent import DryRunControlAgent
from lekiwi_object.agents.vision_agent import SimulatedVisionAgent
from lekiwi_object.agents.voice_agent import TextVoiceAgent
from lekiwi_object.backends import DryRunRobotBackend, RobotBackend
from lekiwi_object.config import AppConfig
from lekiwi_object.models import IntentType, WorkflowResult, WorkflowTrace
from lekiwi_object.simulation import OfflineWorld


class MultiAgentWorkflow:
    def __init__(self, config: AppConfig, robot_backend: RobotBackend | None = None):
        self.config = config
        self.world = OfflineWorld(config.simulation)
        self.voice = TextVoiceAgent()
        self.vision = SimulatedVisionAgent(config.vision, self.world)
        self.control = DryRunControlAgent(config.safety)
        self.robot_backend = robot_backend or DryRunRobotBackend()

    def run_text(self, text: str) -> WorkflowResult:
        return self.run_text_loop(text, steps=1).final

    def run_text_loop(self, text: str, steps: int = 3) -> WorkflowTrace:
        if steps < 1:
            raise ValueError("steps must be >= 1")

        intent = self.voice.parse(text)
        results: list[WorkflowResult] = []
        for step_index in range(steps):
            observation = self.vision.observe(intent)
            command = self.control.plan(intent, observation)
            execution = self.robot_backend.execute(command)
            response = self.voice.render_response(
                intent, _response_for(intent.type, observation.summary, command.name)
            )
            results.append(
                WorkflowResult(
                    intent=intent,
                    observation=observation,
                    command=command,
                    execution=execution,
                    response=response,
                    step_index=step_index,
                )
            )
            self.world.apply(command)
        return WorkflowTrace(results=results)


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
