import random

import start_sim
from Simulation import MAX_FLOOR

AMOUNT_CALLS = 30

if __name__ == "__main__":
    calls = []

    random.seed(999999)
    next_id = 1

    for i in range(1, AMOUNT_CALLS + 1):
        call = {}
        call['id'] = next_id
        call['after'] = random.randint(0, round(start_sim.SIMULATION_TIMEOUT * 0.75))
        call['floor'] = random.randint(0, MAX_FLOOR)
        call['target_floor'] = random.randint(0, MAX_FLOOR)
        call['is_known_previously'] = False
        next_id += 1

        calls.append(call)
    print calls
