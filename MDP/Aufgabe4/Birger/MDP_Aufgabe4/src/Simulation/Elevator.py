import Simulation
from Simulation.Statuses import ElevatorStatus, DoorStatus, Direction, CallStatus


class Elevator(object):
    'An elevator which transports people vertically in a building.'

    def __init__(self, elevator_id, start_in_floor, scheduler):
        self._id = elevator_id
        self._current_floor = start_in_floor
        self._calls = []
        self._direction = None
        self._status = ElevatorStatus.waiting
        self._door_status = DoorStatus.open
        self._scheduler = scheduler

    def is_driving_in_direction_of(self, floor):
        result = False
        if self._direction == Direction.up:
            result = floor >= self._current_floor
        if self._direction == Direction.down:
            result = floor <= self._current_floor
        return result

    def act(self, env):
        # print ' elevator #' + str(self._id) + " is acting"
        if self._status == ElevatorStatus.waiting and self.stop_in_floors:
            # print '  elevator is getting busy'
            self._status = ElevatorStatus.busy
        elif self._status == ElevatorStatus.busy:
            self._direction = Elevator.get_direction_by_floors(self._current_floor, self.target_floor)
            # print '  target set to floor ' + str(self.target_floor)
            if self._door_status == DoorStatus.open:
                # print '  doors closed'
                self._door_status = DoorStatus.closed
                return
            if self._door_status == DoorStatus.closed:
                target_floor = self.target_floor
                if self._current_floor == target_floor:
                    # print '  target reached'
                    # target_floor is reached
                    # print '  doors opened'
                    self._door_status = DoorStatus.open
                    if not self.is_going_to_drive_in_current_direction():
                        self._direction = None
                    self.update_call_statuses(env.now)
                    self.cleanup_calls()
                    self._calls = self._scheduler.get_priorized_call_list(self)
                    if not self.stop_in_floors:
                        self._status = ElevatorStatus.waiting
                    return
                self._direction = self.get_direction_by_floors(self._current_floor, target_floor)
                if self._direction == Direction.up:
                    # print '  driving up'
                    self._current_floor += 1
                    return
                if self._direction == Direction.down:
                    # print '  driving down'
                    self._current_floor -= 1
                    return
                    # else:
                    # print '  but nothing to do'

    def is_going_to_drive_in_current_direction(self):
        result = False

        for target in self.stop_in_floors:
            if self.direction == Direction.up and target >= self.current_floor:
                result = True
            if self.direction == Direction.down and target < self.current_floor:
                result = True

        return result

    def update_call_statuses(self, now):
        for call in self._calls:
            call.processed_by_elevator = self._id
            call.update_status(self._current_floor, now)

    def cleanup_calls(self):
        calls = list(self._calls)
        for call in calls:
            if call.call_status == CallStatus.done:
                self._calls.remove(call)

    @staticmethod
    def get_direction_by_floors(start_floor, end_floor):
        result = None
        if end_floor is None:
            return None
        if start_floor >= Simulation.MAX_FLOOR:
            result = Direction.down
        if start_floor < end_floor:
            result = Direction.up
        if start_floor >= end_floor:
            result = Direction.down
        return result

    @property
    def id(self):
        return self._id

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
            if elevator_call.is_already_known(Simulation.env.now):
                result.append(elevator_call.next_relevant_floor)
            else:
                if elevator_call.will_be_previously_known and elevator_call.call_status == CallStatus.open:
                    result.append(elevator_call.next_relevant_floor)
        return result

    @property
    def direction(self):
        return self._direction
