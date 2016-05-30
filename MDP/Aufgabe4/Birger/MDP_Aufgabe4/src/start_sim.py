import simpy

from Simulation.ElevatorScheduler import ElevatorScheduler, ElevatorCall

SIMULATION_TIMEOUT = 15


class Simulation:
    SIMULATION_TIMESTEP = 1
    AMOUNT_ELEVATORS = 1

    _elevator_calls = [
        {'target_floor': 2, 'after': 5},
        {'target_floor': 1, 'after': 5}
    ]
    _all_happened_elevator_calls = []

    def __init__(self, env):
        self._env = env
        self._elevator_scheduler = ElevatorScheduler(self.AMOUNT_ELEVATORS)

    def run_simulation(self):
        while True:
            self._elevator_scheduler.do_every_timestep(env)
            yield self._env.timeout(self.SIMULATION_TIMESTEP)

    def add_elevator_call(self):
        for elevator_call in self._elevator_calls:
            yield self._env.timeout(elevator_call['after'])
            print str(self._env.now) + ': add call'
            new_call = ElevatorCall(elevator_call['target_floor'], self._env.now)
            self._all_happened_elevator_calls.append(new_call)
            self._elevator_scheduler.add_elevator_call(new_call)


if __name__ == "__main__":
    env = simpy.Environment()
    simulation = Simulation(env)

    print 'add elevator-scheduler to simulation'
    simulation_process = env.process(simulation.run_simulation())

    print 'add elevator calls to simulation'
    elevator_call_process = env.process(simulation.add_elevator_call())

    print 'starting simulation'
    print '#####################'
    print ''
    env.run(until=SIMULATION_TIMEOUT)
