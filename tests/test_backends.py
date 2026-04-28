from lekiwi_object.backends import DryRunRobotBackend
from lekiwi_object.models import ControlCommand


def test_dry_run_backend_records_safe_command():
    backend = DryRunRobotBackend()
    command = ControlCommand(name="no_motion", parameters={}, dry_run=True)
    execution = backend.execute(command)
    assert execution.accepted is True
    assert execution.backend == "dry_run"
    assert backend.history == [command]


def test_dry_run_backend_rejects_live_command():
    backend = DryRunRobotBackend()
    command = ControlCommand(name="center_target", parameters={"theta.vel": 1.0}, dry_run=False)
    execution = backend.execute(command)
    assert execution.accepted is False
    assert "rejected" in execution.message
