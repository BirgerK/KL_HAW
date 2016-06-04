import random

import start_sim

AMOUNT_CALLS = 30

if __name__ == "__main__":
    calls = []

    random.seed(999999)

    for i in range(1, AMOUNT_CALLS + 1):
        call = {}
        call['after'] = random.randint(0, round(start_sim.SIMULATION_TIMEOUT * 0.75))
        call['floor'] = random.randint(0, start_sim.MAX_FLOOR)
        call['target_floor'] = random.randint(0, start_sim.MAX_FLOOR)

        calls.append(call)
    print calls
