import curses

import start_sim

BASE_X = 0
BASE_Y = 0

FLOOR_HEIGHT = 5
FLOOR_WIDTH = 6
FLOOR_MASS_SIZE = 1
FLOOR_MASS = '#'

FLOORNUMBER_SIZE = 1

FLOORNUMBER_DIFF_TO_BOX = 2
FLOORNUMBER_DIFF_MASS = '-'


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

    def update_view(self, elevators):
        scrn = self._screen
        floors_base_x = BASE_X + FLOORNUMBER_SIZE + FLOORNUMBER_DIFF_TO_BOX
        floors_base_y = BASE_Y
        floornumbers_base_x = BASE_X
        floornumbers_base_y = BASE_Y

        scrn.clear()

        self.write_floors(floors_base_x, floors_base_y, len(elevators))
        self.write_floor_numbers(floornumbers_base_x, floornumbers_base_y)
        self.write_elevators(elevators, floors_base_x, floors_base_y)

        scrn.refresh()

    def write_floors(self, base_x, base_y, amount_elevators):
        scrn = self._screen
        max_floor = start_sim.MAX_FLOOR + 1
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
        max_floor = start_sim.MAX_FLOOR + 1

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
        max_floor = start_sim.MAX_FLOOR + 1

        for elevator in elevators:
            elevator_number = elevator.id
            current_floor = elevator.current_floor

            elevator_base_x = box_base_x + ((elevator_number - 1) * FLOOR_WIDTH) + FLOOR_MASS_SIZE
            elevator_base_y = box_base_y + ((max_floor - current_floor - 1) * FLOOR_HEIGHT) + FLOOR_MASS_SIZE

            scrn.addstr(elevator_base_y, elevator_base_x, 'here')
