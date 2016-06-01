import simpy

import Simulation as sim
from Monitoring.Monitoring import plot_calls_done_per_time
from Simulation.Statuses import Direction

SIMULATION_TIMEOUT = 15
SIMULATION_TIMESTEP = 1
AMOUNT_ELEVATORS = 2
MAX_FLOOR = 10

elevator_calls = [
    {'floor': 2, 'target_floor': 0, 'direction': Direction.down, 'after': 5},
    {'floor': 1, 'target_floor': 0, 'direction': Direction.down, 'after': 5}
]
all_happened_elevator_calls = []


def run_simulation():
    while True:
        print str(env.now) + ': '
        elevator_scheduler.do_every_timestep(env)
        yield env.timeout(SIMULATION_TIMESTEP)


def add_elevator_call():
    for elevator_call in elevator_calls:
        new_call = sim.ElevatorScheduler.ElevatorCall(elevator_call['after'], elevator_call['floor'],
                                                      elevator_call['target_floor'], env.now)
        env.process(add_elevator_call_process(new_call))


def add_elevator_call_process(elevator_call):
    yield env.timeout(elevator_call.open_at)
    print str(env.now) + ': add call'
    all_happened_elevator_calls.append(elevator_call)
    elevator_scheduler.add_elevator_call(elevator_call)


if __name__ == "__main__":
    env = simpy.Environment()
    elevator_scheduler = sim.ElevatorScheduler.ElevatorScheduler(AMOUNT_ELEVATORS)

    print 'add elevator-scheduler to simulation'
    simulation_process = env.process(run_simulation())

    print 'add elevator calls to simulation'
    add_elevator_call()

    print 'starting simulation'
    print '#####################'
    print ''
    env.run(until=SIMULATION_TIMEOUT)
    print ''
    print '#####################'
    print 'end simulation'
    plot_calls_done_per_time(all_happened_elevator_calls)
