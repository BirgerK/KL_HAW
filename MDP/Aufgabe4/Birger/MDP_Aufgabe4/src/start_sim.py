import json
import signal
import sys
import time

import simpy
from enum import Enum

import Monitoring.Monitoring as monitor
import Monitoring.UserInterface
import Simulation as sim

SIMULATION_TIMESTEP = 1

use_interface = False

elevator_calls = [{'target_floor': 6, 'is_known_previously': False, 'after': 2, 'id': 1, 'floor': 1},
                  {'target_floor': 7, 'is_known_previously': False, 'after': 4, 'id': 2, 'floor': 5},
                  {'target_floor': 7, 'is_known_previously': False, 'after': 6, 'id': 3, 'floor': 1},
                  {'target_floor': 6, 'is_known_previously': False, 'after': 8, 'id': 4, 'floor': 4},
                  {'target_floor': 3, 'is_known_previously': False, 'after': 10, 'id': 5, 'floor': 7},
                  {'target_floor': 1, 'is_known_previously': False, 'after': 12, 'id': 6, 'floor': 0},
                  {'target_floor': 2, 'is_known_previously': False, 'after': 14, 'id': 7, 'floor': 8},
                  {'target_floor': 3, 'is_known_previously': False, 'after': 16, 'id': 8, 'floor': 5},
                  {'target_floor': 4, 'is_known_previously': False, 'after': 18, 'id': 9, 'floor': 8},
                  {'target_floor': 6, 'is_known_previously': False, 'after': 20, 'id': 10, 'floor': 1},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 22, 'id': 11, 'floor': 2},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 24, 'id': 12, 'floor': 1},
                  {'target_floor': 7, 'is_known_previously': False, 'after': 26, 'id': 13, 'floor': 5},
                  {'target_floor': 4, 'is_known_previously': False, 'after': 28, 'id': 14, 'floor': 3},
                  {'target_floor': 3, 'is_known_previously': False, 'after': 30, 'id': 15, 'floor': 1},
                  {'target_floor': 8, 'is_known_previously': False, 'after': 32, 'id': 16, 'floor': 7},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 34, 'id': 17, 'floor': 3},
                  {'target_floor': 6, 'is_known_previously': False, 'after': 36, 'id': 18, 'floor': 4},
                  {'target_floor': 6, 'is_known_previously': False, 'after': 38, 'id': 19, 'floor': 8},
                  {'target_floor': 3, 'is_known_previously': False, 'after': 40, 'id': 20, 'floor': 0},
                  {'target_floor': 8, 'is_known_previously': False, 'after': 42, 'id': 21, 'floor': 0},
                  {'target_floor': 7, 'is_known_previously': False, 'after': 44, 'id': 22, 'floor': 2},
                  {'target_floor': 2, 'is_known_previously': False, 'after': 46, 'id': 23, 'floor': 4},
                  {'target_floor': 7, 'is_known_previously': False, 'after': 48, 'id': 24, 'floor': 8},
                  {'target_floor': 2, 'is_known_previously': False, 'after': 50, 'id': 25, 'floor': 7},
                  {'target_floor': 4, 'is_known_previously': False, 'after': 52, 'id': 26, 'floor': 8},
                  {'target_floor': 5, 'is_known_previously': False, 'after': 54, 'id': 27, 'floor': 0},
                  {'target_floor': 8, 'is_known_previously': False, 'after': 56, 'id': 28, 'floor': 2},
                  {'target_floor': 3, 'is_known_previously': False, 'after': 58, 'id': 29, 'floor': 8},
                  {'target_floor': 1, 'is_known_previously': False, 'after': 60, 'id': 30, 'floor': 6},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 62, 'id': 31, 'floor': 7},
                  {'target_floor': 4, 'is_known_previously': False, 'after': 64, 'id': 32, 'floor': 5},
                  {'target_floor': 1, 'is_known_previously': False, 'after': 66, 'id': 33, 'floor': 5},
                  {'target_floor': 5, 'is_known_previously': False, 'after': 68, 'id': 34, 'floor': 2},
                  {'target_floor': 5, 'is_known_previously': False, 'after': 70, 'id': 35, 'floor': 3},
                  {'target_floor': 8, 'is_known_previously': False, 'after': 72, 'id': 36, 'floor': 6},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 74, 'id': 37, 'floor': 3},
                  {'target_floor': 4, 'is_known_previously': False, 'after': 76, 'id': 38, 'floor': 2},
                  {'target_floor': 1, 'is_known_previously': False, 'after': 78, 'id': 39, 'floor': 6},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 80, 'id': 40, 'floor': 2},
                  {'target_floor': 2, 'is_known_previously': False, 'after': 82, 'id': 41, 'floor': 0},
                  {'target_floor': 6, 'is_known_previously': False, 'after': 84, 'id': 42, 'floor': 3},
                  {'target_floor': 4, 'is_known_previously': False, 'after': 86, 'id': 43, 'floor': 5},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 88, 'id': 44, 'floor': 1},
                  {'target_floor': 1, 'is_known_previously': False, 'after': 90, 'id': 45, 'floor': 2},
                  {'target_floor': 4, 'is_known_previously': False, 'after': 92, 'id': 46, 'floor': 3},
                  {'target_floor': 1, 'is_known_previously': False, 'after': 94, 'id': 47, 'floor': 3},
                  {'target_floor': 7, 'is_known_previously': False, 'after': 96, 'id': 48, 'floor': 0},
                  {'target_floor': 2, 'is_known_previously': False, 'after': 98, 'id': 49, 'floor': 5},
                  {'target_floor': 8, 'is_known_previously': False, 'after': 100, 'id': 50, 'floor': 6},
                  {'target_floor': 3, 'is_known_previously': False, 'after': 102, 'id': 51, 'floor': 5},
                  {'target_floor': 6, 'is_known_previously': True, 'after': 104, 'id': 52, 'floor': 0},
                  {'target_floor': 3, 'is_known_previously': False, 'after': 106, 'id': 53, 'floor': 0},
                  {'target_floor': 8, 'is_known_previously': False, 'after': 108, 'id': 54, 'floor': 1},
                  {'target_floor': 6, 'is_known_previously': False, 'after': 110, 'id': 55, 'floor': 3},
                  {'target_floor': 2, 'is_known_previously': False, 'after': 112, 'id': 56, 'floor': 6},
                  {'target_floor': 7, 'is_known_previously': False, 'after': 114, 'id': 57, 'floor': 6},
                  {'target_floor': 2, 'is_known_previously': False, 'after': 116, 'id': 58, 'floor': 5},
                  {'target_floor': 2, 'is_known_previously': True, 'after': 118, 'id': 59, 'floor': 6},
                  {'target_floor': 7, 'is_known_previously': False, 'after': 120, 'id': 60, 'floor': 8},
                  {'target_floor': 5, 'is_known_previously': False, 'after': 122, 'id': 61, 'floor': 4},
                  {'target_floor': 6, 'is_known_previously': False, 'after': 124, 'id': 62, 'floor': 5},
                  {'target_floor': 5, 'is_known_previously': False, 'after': 126, 'id': 63, 'floor': 4},
                  {'target_floor': 6, 'is_known_previously': False, 'after': 128, 'id': 64, 'floor': 3},
                  {'target_floor': 6, 'is_known_previously': False, 'after': 130, 'id': 65, 'floor': 0},
                  {'target_floor': 1, 'is_known_previously': False, 'after': 132, 'id': 66, 'floor': 2},
                  {'target_floor': 7, 'is_known_previously': False, 'after': 134, 'id': 67, 'floor': 1},
                  {'target_floor': 2, 'is_known_previously': False, 'after': 136, 'id': 68, 'floor': 8},
                  {'target_floor': 5, 'is_known_previously': False, 'after': 138, 'id': 69, 'floor': 7},
                  {'target_floor': 2, 'is_known_previously': False, 'after': 140, 'id': 70, 'floor': 6},
                  {'target_floor': 8, 'is_known_previously': False, 'after': 142, 'id': 71, 'floor': 0},
                  {'target_floor': 1, 'is_known_previously': False, 'after': 144, 'id': 72, 'floor': 5},
                  {'target_floor': 4, 'is_known_previously': False, 'after': 146, 'id': 73, 'floor': 2},
                  {'target_floor': 2, 'is_known_previously': True, 'after': 148, 'id': 74, 'floor': 7},
                  {'target_floor': 3, 'is_known_previously': False, 'after': 150, 'id': 75, 'floor': 5},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 152, 'id': 76, 'floor': 4},
                  {'target_floor': 2, 'is_known_previously': False, 'after': 154, 'id': 77, 'floor': 7},
                  {'target_floor': 8, 'is_known_previously': False, 'after': 156, 'id': 78, 'floor': 3},
                  {'target_floor': 6, 'is_known_previously': False, 'after': 158, 'id': 79, 'floor': 8},
                  {'target_floor': 2, 'is_known_previously': False, 'after': 160, 'id': 80, 'floor': 5},
                  {'target_floor': 7, 'is_known_previously': False, 'after': 162, 'id': 81, 'floor': 3},
                  {'target_floor': 3, 'is_known_previously': False, 'after': 164, 'id': 82, 'floor': 2},
                  {'target_floor': 1, 'is_known_previously': True, 'after': 166, 'id': 83, 'floor': 2},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 168, 'id': 84, 'floor': 3},
                  {'target_floor': 5, 'is_known_previously': False, 'after': 170, 'id': 85, 'floor': 2},
                  {'target_floor': 5, 'is_known_previously': False, 'after': 172, 'id': 86, 'floor': 7},
                  {'target_floor': 2, 'is_known_previously': False, 'after': 174, 'id': 87, 'floor': 8},
                  {'target_floor': 5, 'is_known_previously': False, 'after': 176, 'id': 88, 'floor': 4},
                  {'target_floor': 4, 'is_known_previously': False, 'after': 178, 'id': 89, 'floor': 3},
                  {'target_floor': 1, 'is_known_previously': False, 'after': 180, 'id': 90, 'floor': 7},
                  {'target_floor': 7, 'is_known_previously': False, 'after': 182, 'id': 91, 'floor': 4},
                  {'target_floor': 4, 'is_known_previously': False, 'after': 184, 'id': 92, 'floor': 6},
                  {'target_floor': 6, 'is_known_previously': False, 'after': 186, 'id': 93, 'floor': 4},
                  {'target_floor': 6, 'is_known_previously': False, 'after': 188, 'id': 94, 'floor': 5},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 190, 'id': 95, 'floor': 6},
                  {'target_floor': 8, 'is_known_previously': False, 'after': 192, 'id': 96, 'floor': 5},
                  {'target_floor': 8, 'is_known_previously': False, 'after': 194, 'id': 97, 'floor': 6},
                  {'target_floor': 1, 'is_known_previously': False, 'after': 196, 'id': 98, 'floor': 2},
                  {'target_floor': 5, 'is_known_previously': False, 'after': 198, 'id': 99, 'floor': 7}]


def run_simulation():
    while True:
        # print str(env.now) + ': '
        elevator_scheduler.do_every_timestep(sim.env)
        if use_interface:
            ui.update_view(elevator_scheduler.elevators, elevator_scheduler.elevator_calls, sim.env)
            time.sleep(1)
        monitor.collect_calls_on_time(sim.env.now, all_happened_elevator_calls)
        yield sim.env.timeout(SIMULATION_TIMESTEP)


def add_elevator_call():
    for elevator_call in elevator_calls:
        new_call = sim.ElevatorScheduler.ElevatorCall(elevator_call['id'], elevator_call['after'],
                                                      elevator_call['floor'],
                                                      elevator_call['target_floor'], sim.env.now,
                                                      elevator_call['is_known_previously'])
        sim.env.process(add_elevator_call_process(new_call))


def add_elevator_call_process(elevator_call):
    if not elevator_call.will_be_previously_known:
        yield sim.env.timeout(elevator_call.open_at)
    # print str(env.now) + ': add call: ' + str(elevator_call.__dict__)
    elevator_call.opened_at = sim.env.now
    all_happened_elevator_calls.append(elevator_call)
    elevator_scheduler.add_elevator_call(elevator_call)


def terminate(signal, frame):
    print 'catch SIGINT, end simulation'


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name
        return json.JSONEncoder.default(self, obj)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, terminate)
    if sys.stdout.isatty():
        use_interface = True
    else:
        use_interface = False
    call_ids_known_previously = []
    for raw_call in elevator_calls:
        if raw_call['is_known_previously']:
            call_ids_known_previously.append(raw_call['id'])

    previously_known_statuses = [False]
    if not use_interface:
        previously_known_statuses.append(True)
    calls_known_previously = {}
    for previously_known_status in previously_known_statuses:
        calls_known_previously[previously_known_status] = []
        for raw_call in elevator_calls:
            if raw_call['id'] in call_ids_known_previously:
                raw_call['is_known_previously'] = previously_known_status
        all_happened_elevator_calls = []
        sim.env = simpy.Environment()
        elevator_scheduler = sim.ElevatorScheduler.ElevatorScheduler(sim.AMOUNT_ELEVATORS)

        # print 'add elevator-scheduler to simulation'
        simulation_process = sim.env.process(run_simulation())

        # print 'add elevator calls to simulation'
        add_elevator_call()

        # print 'init interface'
        if use_interface:
            ui = Monitoring.UserInterface.UserInterface()

        # print 'starting simulation'
        # print '#####################'
        # print ''
        sim.env.run(until=sim.SIMULATION_TIMEOUT)
        # print ''
        # print '#####################'
        # print 'end simulation'
        for call in all_happened_elevator_calls:
            if call.id in call_ids_known_previously:
                calls_known_previously[previously_known_status].append(call.__dict__)

    print json.dumps(calls_known_previously, cls=EnumEncoder, sort_keys=True, indent=2, separators=(',', ': '))

    if use_interface:
        ui.close_terminal()

    if True:
        monitor.plot_calls_done_per_time()
        monitor.plot_waitingtime_per_time()
        monitor.plot_takeawaytime_per_time()
        monitor.show_plots()
