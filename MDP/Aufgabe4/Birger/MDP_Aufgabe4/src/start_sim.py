import signal
import time

import simpy

import Monitoring.UserInterface
import Simulation as sim
from Simulation.Statuses import Direction

SIMULATION_TIMEOUT = 50
SIMULATION_TIMESTEP = 1
AMOUNT_ELEVATORS = 3
MAX_FLOOR = 8

USE_INTERFACE = False

elevator_calls = [{'target_floor': 5, 'direction': 1, 'after': 8, 'floor': 6},
                  {'target_floor': 4, 'direction': 1, 'after': 8, 'floor': 7},
                  {'target_floor': 3, 'direction': 0, 'after': 30, 'floor': 7},
                  {'target_floor': 8, 'direction': 0, 'after': 6, 'floor': 8},
                  {'target_floor': 8, 'direction': 1, 'after': 23, 'floor': 3},
                  {'target_floor': 2, 'direction': 0, 'after': 7, 'floor': 6},
                  {'target_floor': 5, 'direction': 1, 'after': 6, 'floor': 0},
                  {'target_floor': 1, 'direction': 0, 'after': 17, 'floor': 4},
                  {'target_floor': 3, 'direction': 0, 'after': 33, 'floor': 8},
                  {'target_floor': 8, 'direction': 1, 'after': 21, 'floor': 6},
                  {'target_floor': 0, 'direction': 1, 'after': 3, 'floor': 3},
                  {'target_floor': 4, 'direction': 0, 'after': 9, 'floor': 7},
                  {'target_floor': 7, 'direction': 0, 'after': 35, 'floor': 7},
                  {'target_floor': 0, 'direction': 1, 'after': 34, 'floor': 4},
                  {'target_floor': 8, 'direction': 1, 'after': 10, 'floor': 2},
                  {'target_floor': 6, 'direction': 0, 'after': 37, 'floor': 3},
                  {'target_floor': 5, 'direction': 1, 'after': 30, 'floor': 0},
                  {'target_floor': 2, 'direction': 1, 'after': 22, 'floor': 1},
                  {'target_floor': 6, 'direction': 1, 'after': 14, 'floor': 5},
                  {'target_floor': 2, 'direction': 1, 'after': 14, 'floor': 0},
                  {'target_floor': 2, 'direction': 0, 'after': 30, 'floor': 1},
                  {'target_floor': 3, 'direction': 1, 'after': 3, 'floor': 2},
                  {'target_floor': 4, 'direction': 0, 'after': 25, 'floor': 5},
                  {'target_floor': 1, 'direction': 0, 'after': 2, 'floor': 2},
                  {'target_floor': 1, 'direction': 0, 'after': 19, 'floor': 3},
                  {'target_floor': 2, 'direction': 1, 'after': 32, 'floor': 5},
                  {'target_floor': 3, 'direction': 0, 'after': 36, 'floor': 5},
                  {'target_floor': 3, 'direction': 0, 'after': 27, 'floor': 0},
                  {'target_floor': 6, 'direction': 1, 'after': 36, 'floor': 3},
                  {'target_floor': 7, 'direction': 1, 'after': 9, 'floor': 6}]

all_happened_elevator_calls = []


def run_simulation():
    while True:
        # print str(env.now) + ': '
        elevator_scheduler.do_every_timestep(env)
        if USE_INTERFACE:
            ui.update_view(elevator_scheduler.elevators)
            time.sleep(1)
        yield env.timeout(SIMULATION_TIMESTEP)


def add_elevator_call():
    for elevator_call in elevator_calls:
        if elevator_call['direction']:
            direction = Direction.up
        else:
            direction = Direction.down
        new_call = sim.ElevatorScheduler.ElevatorCall(elevator_call['after'], elevator_call['floor'],
                                                      elevator_call['target_floor'], env.now)
        env.process(add_elevator_call_process(new_call))


def add_elevator_call_process(elevator_call):
    yield env.timeout(elevator_call.open_at)
    # print str(env.now) + ': add call: ' + str(elevator_call.__dict__)
    all_happened_elevator_calls.append(elevator_call)
    elevator_scheduler.add_elevator_call(elevator_call)


def terminate(signal, frame):
    print 'catch SIGINT, end simulation'

if __name__ == "__main__":
    signal.signal(signal.SIGINT, terminate)

    env = simpy.Environment()
    elevator_scheduler = sim.ElevatorScheduler.ElevatorScheduler(AMOUNT_ELEVATORS)

    # print 'add elevator-scheduler to simulation'
    simulation_process = env.process(run_simulation())

    # print 'add elevator calls to simulation'
    add_elevator_call()

    # print 'init interface'
    if USE_INTERFACE:
        ui = Monitoring.UserInterface.UserInterface()

    # print 'starting simulation'
    # print '#####################'
    # print ''
    env.run(until=SIMULATION_TIMEOUT)
    # print ''
    # print '#####################'
    # print 'end simulation'
    # monitor.plot_calls_done_per_time(all_happened_elevator_calls)
