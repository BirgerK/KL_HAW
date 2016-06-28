import json

from enum import Enum


class ElevatorStatus(Enum):
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)
    waiting = 'waiting'
    busy = 'busy'


class DoorStatus(Enum):
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)
    open = 'open'
    closed = 'closed'


class Direction(Enum):
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)
    up = 'up'
    down = 'down'


class CallStatus(Enum):
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)
    open = 'open'
    pickup = 'pickup'
    takeaway = 'takeaway'
    done = 'done'
    duplicate = 'duplicate'
