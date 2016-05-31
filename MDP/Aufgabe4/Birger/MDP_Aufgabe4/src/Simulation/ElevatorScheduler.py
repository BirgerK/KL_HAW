import Queue
import sys

from Simulation.Elevator import Elevator
from Simulation.Statuses import CallStatus, Direction


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
            elevator_call = self._elevator_calls.get()
            if self.is_duplicate_call(elevator_call):
                elevator_call.call_status = CallStatus.duplicate
            else:
                fastest_elevator_for_call = self.get_fastest_elevator_for_call(elevator_call)
                fastest_elevator_for_call.set_calls(
                    self.get_sorted_call_into_calls(fastest_elevator_for_call, elevator_call))

    def is_duplicate_call(self, elevator_call):
        result = False
        for elevator in self._elevators:
            if elevator_call in elevator.calls:
                result = True
                break
        return result

    def get_fastest_elevator_for_call(self, elevator_call):
        shortest_time = sys.maxint
        fastest_elevator = None

        for elevator in self._elevators:
            estimated_costs = 0
            new_call_list = self.get_sorted_call_into_calls(elevator, elevator_call)
            estimated_costs += self.get_time_until_call_is_done(elevator.current_floor, new_call_list, elevator_call)
            estimated_costs += self.get_latency_for_calls_behind_call(elevator.current_floor, new_call_list,
                                                                      elevator_call)
            if estimated_costs < shortest_time:
                shortest_time = estimated_costs
                fastest_elevator = elevator
        return fastest_elevator

    def get_sorted_call_into_calls(self, elevator, elevator_call):
        if not elevator.calls:
            return [elevator_call]
        else:
            calls = list(elevator.calls)
            current_floor = elevator.current_floor
            if elevator.direction == Direction.up and elevator_call.target_floor >= current_floor:
                for temp_call in calls:
                    if elevator_call.target_floor < temp_call.target_floor:
                        calls.insert(calls.index(temp_call), elevator_call)
                        break
            elif elevator.direction == Direction.down and elevator_call.target_floor <= current_floor:
                for temp_call in calls:
                    if elevator_call.target_floor > temp_call.target_floor:
                        calls.insert(calls.index(temp_call), elevator_call)
                        break
            else:
                if elevator.direction is None:
                    # elevator is not driving now. we have to assume a direction
                    assumed_direction = Elevator.get_direction_by_floors(elevator.current_floor,
                                                                         elevator.calls[0].target_floor)
                    if assumed_direction == Direction.up and elevator_call.target_floor >= current_floor:
                        for temp_call in calls:
                            if elevator_call.target_floor < temp_call.target_floor:
                                calls.insert(calls.index(temp_call), elevator_call)
                                break
                    elif assumed_direction == Direction.down and elevator_call.target_floor <= current_floor:
                        for temp_call in calls:
                            if elevator_call.target_floor > temp_call.target_floor:
                                calls.insert(calls.index(temp_call), elevator_call)
                                break
                    else:
                        calls.append(elevator_call)
            return calls

    def get_latency_for_calls_behind_call(self, current_floor, elevator_calls, elevator_call):
        calls_behind_call = elevator_calls[elevator_calls.index(elevator_call): len(elevator_calls) + 1]
        time_until_call_is_done = self.get_time_until_call_is_done(current_floor, elevator_calls, elevator_call)

        return time_until_call_is_done * len(calls_behind_call)

    def get_time_until_call_is_done(self, current_floor, elevator_calls, elevator_call):
        calls_must_be_done_before_call = elevator_calls[0:elevator_calls.index(elevator_call) + 1]

        time = 0
        for call in calls_must_be_done_before_call:
            time += self.estimate_driving_time(current_floor, call.target_floor)
            time += 2  # time for closing and opening doors

        return time

    def estimate_driving_time(self, current_floor, target_floor):
        return abs(current_floor - target_floor)


class ElevatorCall:
    def __init__(self, open_at, target_floor, opened_at):
        self._target_floor = target_floor
        self._call_status = CallStatus.open
        self._open_at = open_at
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
    def open_at(self):
        return self._open_at

    @property
    def opened_at(self):
        return self._opened_at

    @property
    def closed_at(self):
        return self._closed_at

    @closed_at.setter
    def closed_at(self, value):
        self._closed_at = value
