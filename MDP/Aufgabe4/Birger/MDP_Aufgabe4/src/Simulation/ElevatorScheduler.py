import Queue

from Simulation.Elevator import Elevator
from Simulation.Statuses import CallStatus, ElevatorStatus


class ElevatorScheduler:
    'A scheduler for elevators'

    def __init__(self, amount_elevators):
        self._elevators = []
        self._elevator_calls = Queue.Queue()
        for elevator_number in range(1, amount_elevators + 1):
            self._elevators.append(Elevator(elevator_number, 0))

    def do_every_timestep(self, env):
        print str(env.now) + ': do scheduler-stuff'
        self.schedule_elevator_calls()
        self.let_elevators_act(env)

    def add_elevator_call(self, call):
        self._elevator_calls.put(call)

    def let_elevators_act(self, env):
        for elevator in self._elevators:
            elevator.act(env)

    def schedule_elevator_calls(self):
        while not self._elevator_calls.empty():
            for elevator in self._elevators:
                if elevator.status == ElevatorStatus.waiting:
                    elevator_call = self._elevator_calls.get()
                    elevator.add_floor_to_targets(elevator_call)


class ElevatorCall:
    def __init__(self, target_floor, opened_at):
        self._target_floor = target_floor
        self._call_status = CallStatus.open
        self._opened_at = opened_at
        self._closed_at = None

    @property
    def target_floor(self):
        return self._target_floor

    @property
    def call_status(self):
        return self._call_status

    @call_status.setter
    def call_status(self, value):
        self._call_status = value

    @property
    def closed_at(self):
        return self._closed_at

    @closed_at.setter
    def closed_at(self, value):
        self._closed_at = value
