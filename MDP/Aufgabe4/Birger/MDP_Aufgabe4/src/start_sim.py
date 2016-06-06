import signal
import sys
import time

import simpy

import Monitoring.Monitoring as monitor
import Monitoring.UserInterface
import Simulation as sim

SIMULATION_TIMEOUT = 70
SIMULATION_TIMESTEP = 1

use_interface = False

elevator_calls = [{'target_floor': 5, 'is_known_previously': False, 'after': 11, 'id': 1, 'floor': 6},
                  {'target_floor': 7, 'is_known_previously': False, 'after': 44, 'id': 2, 'floor': 1},
                  {'target_floor': 7, 'is_known_previously': False, 'after': 29, 'id': 3, 'floor': 6},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 47, 'id': 4, 'floor': 3},
                  {'target_floor': 8, 'is_known_previously': False, 'after': 8, 'id': 5, 'floor': 8},
                  {'target_floor': 3, 'is_known_previously': False, 'after': 16, 'id': 6, 'floor': 5},
                  {'target_floor': 1, 'is_known_previously': False, 'after': 50, 'id': 7, 'floor': 4},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 39, 'id': 8, 'floor': 2},
                  {'target_floor': 5, 'is_known_previously': False, 'after': 9, 'id': 9, 'floor': 0},
                  {'target_floor': 4, 'is_known_previously': False, 'after': 42, 'id': 10, 'floor': 3},
                  {'target_floor': 7, 'is_known_previously': False, 'after': 7, 'id': 11, 'floor': 3},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 48, 'id': 12, 'floor': 3},
                  {'target_floor': 8, 'is_known_previously': False, 'after': 29, 'id': 13, 'floor': 6},
                  {'target_floor': 3, 'is_known_previously': False, 'after': 36, 'id': 14, 'floor': 0},
                  {'target_floor': 2, 'is_known_previously': False, 'after': 3, 'id': 15, 'floor': 8},
                  {'target_floor': 2, 'is_known_previously': False, 'after': 44, 'id': 16, 'floor': 4},
                  {'target_floor': 7, 'is_known_previously': False, 'after': 48, 'id': 17, 'floor': 7},
                  {'target_floor': 4, 'is_known_previously': False, 'after': 14, 'id': 18, 'floor': 8},
                  {'target_floor': 2, 'is_known_previously': False, 'after': 2, 'id': 19, 'floor': 5},
                  {'target_floor': 8, 'is_known_previously': False, 'after': 17, 'id': 20, 'floor': 8},
                  {'target_floor': 6, 'is_known_previously': False, 'after': 52, 'id': 21, 'floor': 3},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 9, 'id': 22, 'floor': 7},
                  {'target_floor': 5, 'is_known_previously': False, 'after': 31, 'id': 23, 'floor': 4},
                  {'target_floor': 5, 'is_known_previously': False, 'after': 7, 'id': 24, 'floor': 2},
                  {'target_floor': 6, 'is_known_previously': False, 'after': 20, 'id': 25, 'floor': 5},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 49, 'id': 26, 'floor': 3},
                  {'target_floor': 6, 'is_known_previously': False, 'after': 16, 'id': 27, 'floor': 4},
                  {'target_floor': 0, 'is_known_previously': False, 'after': 7, 'id': 28, 'floor': 2},
                  {'target_floor': 3, 'is_known_previously': False, 'after': 5, 'id': 29, 'floor': 2},
                  {'target_floor': 5, 'is_known_previously': False, 'after': 39, 'id': 30, 'floor': 5}]

all_happened_elevator_calls = []


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
    all_happened_elevator_calls.append(elevator_call)
    elevator_scheduler.add_elevator_call(elevator_call)


def terminate(signal, frame):
    print 'catch SIGINT, end simulation'


if __name__ == "__main__":
    signal.signal(signal.SIGINT, terminate)
    if sys.stdout.isatty():
        use_interface = True
    else:
        use_interface = False

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
    sim.env.run(until=SIMULATION_TIMEOUT)
    # print ''
    # print '#####################'
    # print 'end simulation'
    if use_interface:
        ui.close_terminal()
    monitor.plot_calls_done_per_time()
    monitor.plot_waitingtime_per_time()
    monitor.plot_takeawaytime_per_time()
    monitor.show_plots()
