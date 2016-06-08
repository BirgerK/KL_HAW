import curses

import Simulation as sim

BASE_X = 0
BASE_Y = 0

FLOOR_HEIGHT = 5
FLOOR_WIDTH = 8
FLOOR_MASS_SIZE = 1
FLOOR_MASS = '#'

FLOORNUMBER_SIZE = 1

FLOORNUMBER_DIFF_TO_BOX = 2
FLOORNUMBER_DIFF_MASS = '-'

STATUSBOX_DIFF_TO_ELEVATORBOX = 5

ELEVATORSTATUSBOX_WIDTH = 10
ELEVATORSTATUSBOX_HEIGHT = 5
ELEVATORSTATUSBOX_MASS = '#'


class UserInterface:
    def __init__(self):
        self._screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self._screen.keypad(True)

    def close_terminal(self):
        curses.nocbreak()
        self._screen.keypad(False)
        curses.echo()
        curses.endwin()

    def update_view(self, elevators, elevator_calls, env):
        scrn = self._screen
        max_floor = sim.MAX_FLOOR + 1

        floors_base_x = BASE_X + FLOORNUMBER_SIZE + FLOORNUMBER_DIFF_TO_BOX
        floors_base_y = BASE_Y
        floornumbers_base_x = BASE_X
        floornumbers_base_y = BASE_Y
        statusbox_base_x = floors_base_x + (max_floor * FLOOR_HEIGHT) + STATUSBOX_DIFF_TO_ELEVATORBOX
        statusbox_base_y = BASE_Y

        scrn.clear()

        self.write_floors(floors_base_x, floors_base_y, len(elevators))
        self.write_floor_numbers(floornumbers_base_x, floornumbers_base_y)
        self.write_elevators(elevators, floors_base_x, floors_base_y)
        self.write_status(statusbox_base_x, statusbox_base_y, elevators, elevator_calls, env)

        scrn.refresh()

    def write_floors(self, base_x, base_y, amount_elevators):
        scrn = self._screen
        max_floor = sim.MAX_FLOOR + 1
        for elevator_number in range(0, amount_elevators):
            base_box_x = base_x + (elevator_number * FLOOR_WIDTH)
            for floor in range(1, max_floor + 1):
                base_box_y = base_y + ((floor - 1) * FLOOR_HEIGHT)
                next_base_box_y = base_y + ((floor) * FLOOR_HEIGHT)
                # top border
                for i in range(0, FLOOR_WIDTH):
                    x = base_box_x + i
                    scrn.addstr(base_box_y, x, FLOOR_MASS)
                # left border
                for i in range(base_box_y, next_base_box_y + 1):
                    scrn.addstr(i, base_box_x, FLOOR_MASS)
                # right border
                for i in range(base_box_y, next_base_box_y + 1):
                    scrn.addstr(i, base_box_x + FLOOR_WIDTH, FLOOR_MASS)
            # bottom border
            all_floors_height = base_y + (max_floor * FLOOR_HEIGHT)
            for i in range(0, FLOOR_WIDTH):
                x = base_box_x + i
                scrn.addstr(all_floors_height, x, FLOOR_MASS)

    def write_floor_numbers(self, base_x, base_y):
        scrn = self._screen
        max_floor = sim.MAX_FLOOR + 1

        for floor in range(1, max_floor + 1):
            base_floornumber_y = base_y + (floor * FLOOR_HEIGHT)
            # floor numbers
            scrn.addstr(base_floornumber_y, base_x, str(max_floor - floor))
            # floor number diff to box
            for i in range(1, FLOORNUMBER_DIFF_TO_BOX + 1):
                x = base_x + i
                scrn.addstr(base_floornumber_y, x, FLOORNUMBER_DIFF_MASS)

    def write_elevators(self, elevators, box_base_x, box_base_y):
        scrn = self._screen
        max_floor = sim.MAX_FLOOR + 1

        for elevator in elevators:
            elevator_number = elevator.id
            current_floor = elevator.current_floor
            direction = elevator.direction if not elevator.direction is None else ''
            door_status = elevator.door_status if not elevator.door_status is None else ''

            elevator_base_x = box_base_x + ((elevator_number - 1) * FLOOR_WIDTH) + FLOOR_MASS_SIZE
            elevator_base_y = box_base_y + ((max_floor - current_floor - 1) * FLOOR_HEIGHT) + FLOOR_MASS_SIZE

            scrn.addstr(elevator_base_y, elevator_base_x, str(direction))
            scrn.addstr(elevator_base_y + 1, elevator_base_x, str(door_status))

    def write_status(self, base_x, base_y, elevators, elevator_calls, env):
        scrn = self._screen

        time_str = 'Time: ' + str(env.now)
        scrn.addstr(base_y, base_x, time_str)
        calls_str = 'Call-Queue: [' + ','.join(str(call.next_relevant_floor) for call in elevator_calls) + ']'
        scrn.addstr(base_y + 1, base_x, calls_str)

        for elevator in elevators:
            elevatorstatusbox_y = base_y + 2 + ((elevator.id - 1) * ELEVATORSTATUSBOX_HEIGHT)
            self.write_elevator_status(base_x, elevatorstatusbox_y, elevator)

    def write_elevator_status(self, base_x, base_y, elevator):
        scrn = self._screen
        next_elevatorstatusbox_y = base_y + ELEVATORSTATUSBOX_HEIGHT

        # top border
        for i in range(0, ELEVATORSTATUSBOX_WIDTH):
            x = base_x + i
            scrn.addstr(base_y, x, ELEVATORSTATUSBOX_MASS)
        # left border
        for i in range(base_y, next_elevatorstatusbox_y + 1):
            scrn.addstr(i, base_x, ELEVATORSTATUSBOX_MASS)
        # bottom border
        for i in range(0, ELEVATORSTATUSBOX_WIDTH):
            x = base_x + i
            scrn.addstr(next_elevatorstatusbox_y, x, ELEVATORSTATUSBOX_MASS)

        # content
        statuscontent_x = base_x + 1
        statuscontent_y = base_y + 1

        id_str = 'id: ' + str(elevator.id)
        scrn.addstr(statuscontent_y, statuscontent_x, id_str)
        call_ids = 'call_ids: [' + ','.join(str(call.id) for call in elevator.calls) + ']'
        scrn.addstr(statuscontent_y + 1, statuscontent_x, call_ids)
        target_str = 'targets: ' + str(elevator.stop_in_floors)
        scrn.addstr(statuscontent_y + 2, statuscontent_x, target_str)
