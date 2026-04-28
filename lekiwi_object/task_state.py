from __future__ import annotations

from lekiwi_object.models import (
    ControlCommand,
    FunctionCall,
    FunctionName,
    TaskState,
    TaskStatus,
    VisionObservation,
)


class TaskStateTracker:
    """Derives user-facing task status from the local agent loop."""

    def update(
        self,
        function_call: FunctionCall,
        observation: VisionObservation,
        command: ControlCommand,
    ) -> TaskState:
        if function_call.name == FunctionName.NONE:
            return TaskState(
                name=function_call.name,
                status=TaskStatus.IDLE,
                target=None,
                message="没有足够明确的功能调用。",
            )

        if function_call.name == FunctionName.CHAT:
            return TaskState(
                name=function_call.name,
                status=TaskStatus.COMPLETED,
                target=None,
                message="已完成本地文本对话回复。",
            )

        if function_call.name == FunctionName.DESCRIBE_SCENE:
            return TaskState(
                name=function_call.name,
                status=TaskStatus.COMPLETED,
                target=observation.target,
                message="已完成本地视觉场景识别。",
            )

        if function_call.name == FunctionName.STOP:
            return TaskState(
                name=function_call.name,
                status=TaskStatus.COMPLETED,
                target=observation.target,
                message="已生成停止命令并由 dry-run 后端记录。",
            )

        if function_call.name == FunctionName.TRACK_TARGET:
            if command.name == "hold_target":
                return TaskState(
                    name=function_call.name,
                    status=TaskStatus.COMPLETED,
                    target=observation.target,
                    message="目标已经进入画面中心区域，追踪闭环可保持。",
                )
            return TaskState(
                name=function_call.name,
                status=TaskStatus.RUNNING,
                target=observation.target,
                message="正在通过视觉反馈生成居中控制命令。",
            )

        if function_call.name == FunctionName.TOUCH_TARGET:
            if command.name == "guarded_touch":
                return TaskState(
                    name=function_call.name,
                    status=TaskStatus.RUNNING,
                    target=observation.target,
                    message="已形成受保护触碰计划，当前仍由 dry-run 后端记录。",
                )
            return TaskState(
                name=function_call.name,
                status=TaskStatus.BLOCKED,
                target=observation.target,
                message="触碰任务已识别，但未完成真实手眼标定和安全确认，暂不执行物理动作。",
            )

        return TaskState(
            name=function_call.name,
            status=TaskStatus.FAILED,
            target=observation.target,
            message="任务状态机没有覆盖该功能调用。",
        )
