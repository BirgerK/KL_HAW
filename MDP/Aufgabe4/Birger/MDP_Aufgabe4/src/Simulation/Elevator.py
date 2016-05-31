from Simulation.Statuses import ElevatorStatus, DoorStatus, CallStatus, Direction


class Elevator:
    'An elevator which transports people vertically in a building.'

    def __init__(self, elevator_id, start_in_floor):
        self._id = elevator_id
        self._current_floor = start_in_floor
        self._current_call = None
        self._calls = []
        self._direction = None
        self._status = ElevatorStatus.waiting
        self._door_status = DoorStatus.open

    def add_floor_to_targets(self, target_floor):
        self._calls.append(target_floor)

    def is_open_call_existing(self):
        result = False
        for call in self._calls:
            if call.call_status == CallStatus.open:
                result = True
        return result

    def is_driving_in_direction_of(self, floor):
        result = False
        if self._direction == Direction.up:
            result = floor > self._current_floor
        if self._direction == Direction.down:
            result = floor < self._current_floor
        return result

    def set_calls(self, new_calls):
        self._calls = new_calls
        if self._current_call is None or new_calls[0].target_floor != self._current_call.target_floor:
            self.set_current_call(new_calls[0], False)

    def set_current_call(self, new_call, is_old_call_done):
        if not self._current_call is None:
            if is_old_call_done:
                self._current_call.call_status = CallStatus.done
            else:
                self._current_call.call_status = CallStatus.open
        self._current_call = new_call
        self._current_call.call_status = CallStatus.progress

    def act(self, env):
        print str(env.now) + ': elevator #' + str(self._id) + " is acting"
        if self._status == ElevatorStatus.waiting:
            if self._current_call is None:
                if self.is_open_call_existing():
                    self.set_current_call(self._calls[0], False)
            if not self._current_call is None:
                print ' elevator is getting busy'
                self._status = ElevatorStatus.busy
                print ' target set to floor ' + str(self._current_call.target_floor)
        if self._status == ElevatorStatus.busy:
            if self._door_status == DoorStatus.open:
                print ' doors closed'
                self._door_status = DoorStatus.closed
                return
            if self._door_status == DoorStatus.closed:
                target_floor = self._current_call.target_floor
                if self._current_floor == target_floor:
                    print ' target reached'
                    # target_floor is reached
                    self._status = ElevatorStatus.waiting
                    print ' doors opened'
                    self._door_status = DoorStatus.open
                    print ' call done'
                    self._current_call.call_status = CallStatus.done
                    self._current_call.closed_at = env.now
                    self._calls.remove(self._current_call)
                    self._current_call = None
                    self._direction = None
                    return
                self._direction = self.get_direction_by_floors(self._current_floor, target_floor)
                if self._direction == Direction.up:
                    print ' driving up'
                    self._current_floor += 1
                    return
                if self._direction == Direction.down:
                    print ' driving down'
                    self._current_floor -= 1
                    return

    @staticmethod
    def get_direction_by_floors(start_floor, end_floor):
        result = None
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
    def door_status(self):
        return self._door_status

    @property
    def calls(self):
        return self._calls

    @property
    def direction(self):
        return self._direction
