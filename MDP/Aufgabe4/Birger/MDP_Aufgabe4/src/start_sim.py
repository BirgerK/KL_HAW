import simpy

from Simulation.ElevatorScheduler import ElevatorScheduler, ElevatorCall

SIMULATION_TIMEOUT = 15


class Simulation:
    SIMULATION_TIMESTEP = 1
    AMOUNT_ELEVATORS = 1

    def __init__(self, env):
        self._env = env
        self._elevator_scheduler = ElevatorScheduler(self.AMOUNT_ELEVATORS)

    def run_simulation(self):
        while True:
            self._elevator_scheduler.do_every_timestep(env)
            yield self._env.timeout(self.SIMULATION_TIMESTEP)

    def add_elevator_call(self):
        yield self._env.timeout(5)
        print str(self._env.now) + ': add call'
        self._elevator_scheduler.add_elevator_call(ElevatorCall(1))


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
