
import yaml

from funcytestengine.engine import TaskEngine
from funcytestengine.machine import TaskMachine, STATES


def test_main(file_name):
    with open(file_name) as f:
        state_dict = yaml.load(f)

    machine = TaskMachine(machine_dict=state_dict)
    assert machine.state == STATES.PENDING
    engine = TaskEngine(machine)
    result = engine.run()
    assert result == True
    print(state_dict)
