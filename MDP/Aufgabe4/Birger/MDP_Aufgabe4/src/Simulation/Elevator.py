import Queue

from enum import Enum


class Elevator:
    'An elevator which transports people vertically in a building.'

    def __init__(self, elevator_id, start_in_floor):
        self._id = elevator_id
        self._current_floor = start_in_floor
        self._target_floor = start_in_floor
        self._target_floors = Queue.Queue()
        self._direction = None
        self._status = Status.waiting
        self._door_status = DoorStatus.open

    def add_floor_to_targets(self, target_floor):
        self._target_floors.put(target_floor)

    def act(self, env):
        print str(env.now) + ': elevator #' + str(self._id) + " is acting"
        if self._status == Status.waiting and not self._target_floors.empty():
            print ' elevator is getting busy'
            self._status = Status.busy
            self._target_floor = self._target_floors.get()
            print ' target set to floor ' + str(self._target_floor)
        if self._status == Status.busy:
            if self._door_status == DoorStatus.open:
                print ' doors closed'
                self._door_status = DoorStatus.closed
                return
            if self._door_status == DoorStatus.closed:
                if self._current_floor == self._target_floor:
                    print ' target reached'
                    # target_floor is reached
                    self._status = Status.waiting
                    self._target_floor = None
                    print ' doors opened'
                    self._door_status = DoorStatus.open
                    return
                if self._current_floor < self._target_floor:
                    print ' driving up'
                    # drive a floor up
                    self._current_floor += 1
                    return
                if self._current_floor > self._target_floor:
                    print ' driving down'
                    # drive a floor down
                    self._current_floor -= 1
                    return

    @property
    def status(self):
        return self._status


class Status(Enum):
    waiting = 'waiting'
    busy = 'busy'


class DoorStatus(Enum):
    open = 'open'
    closed = 'closed'

class Direction(Enum):
    up = 'up'
    down = 'down'
