from enum import Enum


class ElevatorStatus(Enum):
    waiting = 'waiting'
    busy = 'busy'


class DoorStatus(Enum):
    open = 'open'
    closed = 'closed'


class Direction(Enum):
    up = 'up'
    down = 'down'


class CallStatus(Enum):
    open = 'open'
    progress = 'progress'
    done = 'done'
    duplicate = 'duplicate'
