import random

from Simulation import MAX_FLOOR, SIMULATION_TIMEOUT

CALLS_PER_TIMEUNIT = 0.5

if __name__ == "__main__":
    calls = []

    random.seed(999999)
    next_id = 1

    call_counter = 0
    for time in range(1, SIMULATION_TIMEOUT):
        call_counter += 1
        if call_counter == int((1 / CALLS_PER_TIMEUNIT)):
            call = {}
            call['id'] = next_id
            call['after'] = time
            call['floor'] = random.randint(0, MAX_FLOOR)
            call['target_floor'] = random.randint(0, MAX_FLOOR)
            while call['floor'] == call['target_floor']:
                call['target_floor'] = random.randint(0, MAX_FLOOR)
            call['is_known_previously'] = False
            next_id += 1

            calls.append(call)
            call_counter = 0
    print calls
