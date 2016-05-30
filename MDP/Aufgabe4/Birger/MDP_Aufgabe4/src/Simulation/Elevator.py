from Simulation.Statuses import ElevatorStatus, DoorStatus, CallStatus


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

    def act(self, env):
        print str(env.now) + ': elevator #' + str(self._id) + " is acting"
        if self._status == ElevatorStatus.waiting and self.is_open_call_existing():
            print ' elevator is getting busy'
            self._status = ElevatorStatus.busy
            self._current_call = self._calls[0]
            self._current_call.call_status = CallStatus.progress
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
                    return
                if self._current_floor < target_floor:
                    print ' driving up'
                    # drive a floor up
                    self._current_floor += 1
                    return
                if self._current_floor > target_floor:
                    print ' driving down'
                    # drive a floor down
                    self._current_floor -= 1
                    return

    @property
    def status(self):
        return self._status