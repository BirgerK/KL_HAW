import Simulation
import start_sim
from Simulation.Statuses import ElevatorStatus, DoorStatus, Direction, CallStatus


class Elevator(object):
    'An elevator which transports people vertically in a building.'

    def __init__(self, elevator_id, start_in_floor):
        self._id = elevator_id
        self._current_floor = start_in_floor
        self._calls = []
        self._direction = None
        self._status = ElevatorStatus.waiting
        self._door_status = DoorStatus.open

    def is_driving_in_direction_of(self, floor):
        result = False
        if self._direction == Direction.up:
            result = floor > self._current_floor
        if self._direction == Direction.down:
            result = floor < self._current_floor
        return result

    def act(self, env):
        print ' elevator #' + str(self._id) + " is acting"
        if self._status == ElevatorStatus.waiting and self.stop_in_floors:
            print '  elevator is getting busy'
            self._status = ElevatorStatus.busy
            print '  target set to floor ' + str(self.target_floor)
        elif self._status == ElevatorStatus.busy:
            if self._door_status == DoorStatus.open:
                print '  doors closed'
                self._door_status = DoorStatus.closed
                return
            if self._door_status == DoorStatus.closed:
                target_floor = self.target_floor
                if self._current_floor == target_floor:
                    print '  target reached'
                    # target_floor is reached
                    self._status = ElevatorStatus.waiting
                    print '  doors opened'
                    self._door_status = DoorStatus.open
                    self.update_call_statuses(env.now)
                    self.cleanup_calls()
                    self._direction = None
                    return
                self._direction = self.get_direction_by_floors(self._current_floor, target_floor)
                if self._direction == Direction.up:
                    print '  driving up'
                    self._current_floor += 1
                    return
                if self._direction == Direction.down:
                    print '  driving down'
                    self._current_floor -= 1
                    return
        else:
            print '  but nothing to do'

    def update_call_statuses(self, now):
        for call in self._calls:
            call.update_status(self._current_floor, now)

    def cleanup_calls(self):
        for call in self._calls:
            if call.call_status == CallStatus.done:
                self._calls.remove(call)

    @staticmethod
    def get_direction_by_floors(start_floor, end_floor):
        result = None
        if end_floor is None:
            return None
        if start_floor >= start_sim.MAX_FLOOR:
            result = Direction.down
        if start_floor < end_floor:
            result = Direction.up
        if start_floor >= end_floor:
            result = Direction.down
        return result

    @property
    def status(self):
        return self._status

    @property
    def current_floor(self):
        return self._current_floor

    @property
    def target_floor(self):
        if self.stop_in_floors:
            return self.stop_in_floors[0]
        else:
            return None

    @property
    def door_status(self):
        return self._door_status

    @property
    def calls(self):
        return self._calls

    @calls.setter
    def calls(self, value):
        self._calls = value

    @property
    def stop_in_floors(self):
        result = []
        for elevator_call in self.calls:
            result.append(elevator_call.next_relevant_floor)
        return result

    @property
    def direction(self):
        return self._direction
