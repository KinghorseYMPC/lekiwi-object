from __future__ import annotations

from lekiwi_object.agents.control_agent import DryRunControlAgent
from lekiwi_object.agents.vision_agent import SimulatedVisionAgent
from lekiwi_object.agents.voice_agent import TextVoiceAgent
from lekiwi_object.backends import DryRunRobotBackend, RobotBackend
from lekiwi_object.config import AppConfig
from lekiwi_object.function_calling import FunctionRouter
from lekiwi_object.models import IntentType, WorkflowResult, WorkflowTrace
from lekiwi_object.simulation import OfflineWorld
from lekiwi_object.speech_io import MockSpeechIO, SpeechIO
from lekiwi_object.task_state import TaskStateTracker
from lekiwi_object.vision_backends import OfflineVisionBackend, VisionBackend


class MultiAgentWorkflow:
    def __init__(
        self,
        config: AppConfig,
        robot_backend: RobotBackend | None = None,
        speech_io: SpeechIO | None = None,
        vision_backend: VisionBackend | None = None,
    ):
        self.config = config
        self.world = OfflineWorld(config.simulation)
        self.speech_io = speech_io or MockSpeechIO(config.voice)
        self.voice = TextVoiceAgent()
        self.router = FunctionRouter()
        self.vision_backend = vision_backend or OfflineVisionBackend(config.vision, self.world)
        self.vision = SimulatedVisionAgent(self.vision_backend)
        self.control = DryRunControlAgent(config.safety)
        self.task_state = TaskStateTracker()
        self.robot_backend = robot_backend or DryRunRobotBackend()

    def run_text(self, text: str) -> WorkflowResult:
        return self.run_text_loop(text, steps=1).final

    def run_text_loop(self, text: str, steps: int = 3) -> WorkflowTrace:
        if steps < 1:
            raise ValueError("steps must be >= 1")

        speech_input = self.speech_io.listen_text(text)
        intent = self.voice.parse(speech_input.transcript)
        function_call = self.router.route(intent)
        results: list[WorkflowResult] = []
        for step_index in range(steps):
            observation = self.vision.observe(intent)
            command = self.control.plan(intent, observation)
            execution = self.robot_backend.execute(command)
            task_state = self.task_state.update(function_call, observation, command)
            response = self.voice.render_response(
                intent, _response_for(intent.type, observation.summary, command.name, task_state.message)
            )
            speech_output = self.speech_io.speak(response)
            results.append(
                WorkflowResult(
                    speech_input=speech_input,
                    intent=intent,
                    function_call=function_call,
                    observation=observation,
                    command=command,
                    execution=execution,
                    task_state=task_state,
                    speech_output=speech_output,
                    response=response,
                    step_index=step_index,
                )
            )
            self.world.apply(command)
        return WorkflowTrace(results=results)


def _response_for(intent_type: IntentType, vision_summary: str, command_name: str, task_message: str) -> str:
    if intent_type == IntentType.DESCRIBE_SCENE:
        return vision_summary
    if intent_type == IntentType.TRACK_TARGET:
        return f"{vision_summary} 我会生成 {command_name} 指令让目标回到画面中心。{task_message}"
    if intent_type == IntentType.TOUCH_TARGET:
        return f"{vision_summary} {task_message}"
    if intent_type == IntentType.STOP:
        return task_message
    return "收到。"
