import Queue
import sys

from Simulation.Elevator import Elevator
from Simulation.Statuses import CallStatus, Direction


class ElevatorScheduler(object):
    'A scheduler for elevators'

    def __init__(self, amount_elevators):
        self._elevators = []
        self._elevator_calls = Queue.Queue()
        for elevator_number in range(1, amount_elevators + 1):
            self._elevators.append(Elevator(elevator_number, 0, self))

    def do_every_timestep(self, env):
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
                fastest_elevator_for_call.calls = self.get_sorted_call_into_calls(fastest_elevator_for_call,
                                                                                  fastest_elevator_for_call.calls,
                                                                                  elevator_call)

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
            new_call_list = self.get_sorted_call_into_calls(elevator, elevator.calls, elevator_call)
            estimated_costs += self.get_time_until_call_is_done(elevator.current_floor, new_call_list, elevator_call)
            estimated_costs += self.get_latency_for_calls_behind_call(elevator.current_floor, new_call_list,
                                                                      elevator_call)
            if estimated_costs < shortest_time:
                shortest_time = estimated_costs
                fastest_elevator = elevator
        return fastest_elevator

    def get_priorized_call_list(self, elevator):
        result = []
        for elevator_call in elevator.calls:
            result = ElevatorScheduler.get_sorted_call_into_calls(elevator, result, elevator_call)
        return result

    @staticmethod
    def get_sorted_call_into_calls(elevator, elevator_calls, elevator_call):
        if not elevator.calls:
            return [elevator_call]
        else:
            calls = list(elevator_calls)
            current_floor = elevator.current_floor
            target_floor = elevator_call.next_relevant_floor
            if elevator.direction == Direction.up and target_floor >= current_floor:
                max_floor = -1
                max_floor_index = -1
                for temp_call in calls:
                    if target_floor < temp_call.next_relevant_floor:
                        if temp_call.next_relevant_floor > max_floor:
                            max_floor = temp_call.next_relevant_floor
                            max_floor_index = calls.index(temp_call)
                        calls.insert(calls.index(temp_call), elevator_call)
                        break
                if not elevator_call in calls:
                    calls.insert(max_floor_index + 1, elevator_call)
            elif elevator.direction == Direction.down and target_floor <= current_floor:
                min_floor = sys.maxint
                min_floor_index = sys.maxint
                for temp_call in calls:
                    if temp_call.next_relevant_floor < min_floor:
                        min_floor = temp_call.next_relevant_floor
                        min_floor_index = calls.index(temp_call)
                    if target_floor > temp_call.next_relevant_floor:
                        calls.insert(calls.index(temp_call), elevator_call)
                        break
                if not elevator_call in calls:
                    calls.insert(min_floor_index + 1, elevator_call)
            elif elevator.direction is None:
                # elevator is not driving now. we have to assume a direction
                assumed_direction = Elevator.get_direction_by_floors(elevator.current_floor,
                                                                     elevator.target_floor)
                if assumed_direction == Direction.up and target_floor >= current_floor:
                    max_floor = -1
                    max_floor_index = -1
                    for temp_call in calls:
                        if temp_call.next_relevant_floor > max_floor:
                            max_floor = temp_call.next_relevant_floor
                            max_floor_index = calls.index(temp_call)
                        if target_floor < temp_call.next_relevant_floor:
                            calls.insert(calls.index(temp_call), elevator_call)
                            break
                    if not elevator_call in calls:
                        calls.insert(max_floor_index + 1, elevator_call)
                elif assumed_direction == Direction.down and target_floor <= current_floor:
                    min_floor = sys.maxint
                    min_floor_index = sys.maxint
                    for temp_call in calls:
                        if temp_call.next_relevant_floor < min_floor:
                            min_floor = temp_call.next_relevant_floor
                            min_floor_index = calls.index(temp_call)
                        if target_floor > temp_call.next_relevant_floor:
                            calls.insert(calls.index(temp_call), elevator_call)
                            break
                    if not elevator_call in calls:
                        calls.insert(min_floor_index + 1, elevator_call)
            if not elevator_call in calls:
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
            time += self.estimate_driving_time(current_floor, call.next_relevant_floor)
            time += 2  # time for closing and opening doors

        return time

    def estimate_driving_time(self, current_floor, target_floor):
        return abs(current_floor - target_floor)

    @property
    def elevators(self):
        return self._elevators


class ElevatorCall(object):
    def __init__(self, open_at, call_on_floor, target_floor, opened_at):
        self._call_on_floor = call_on_floor
        self._target_floor = target_floor
        self._call_status = CallStatus.open
        self._open_at = open_at
        self._opened_at = opened_at
        self._takenup_at = None
        self._closed_at = None
        self._processed_by_elevator = None

    def update_status(self, floor_reached, timestamp):
        if self._call_status == CallStatus.open and self._call_on_floor == floor_reached:
            self._call_status = CallStatus.takeaway
            self._takenup_at = timestamp
        if self._call_status == CallStatus.takeaway and self._target_floor == floor_reached:
            # print '  call done'
            self._call_status = CallStatus.done
            self._closed_at = timestamp

    @property
    def next_relevant_floor(self):
        result = None
        if self._call_status == CallStatus.open or self._call_status == CallStatus.pickup:
            result = self._call_on_floor
        if self._call_status == CallStatus.takeaway:
            result = self._target_floor
        return result

    # @property
    # def target_floor(self):
    #     return self._target_floor

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
    def takenup_at(self):
        return self._takenup_at

    @property
    def closed_at(self):
        return self._closed_at

    @closed_at.setter
    def closed_at(self, value):
        self._closed_at = value

    @property
    def processed_by_elevat(self):
        return self._processed_by_elevator

    @processed_by_elevat.setter
    def processed_by_elevat(self, value):
        self._processed_by_elevator = value
