import matplotlib.pyplot as plt
import collections

from Simulation.Statuses import CallStatus


def get_average_waiting_time(elevator_calls):
    sum = 0
    amount = 0
    for elevator_call in elevator_calls:
        if elevator_call.call_status == CallStatus.done or elevator_call.call_status == CallStatus.takeaway:
            sum += (elevator_call.takenup_at - elevator_call.opened_at)
            amount += 1
    if sum == 0 or amount == 0:
        average_waiting_time = 0
    else:
        average_waiting_time = sum / amount
    return average_waiting_time


def plot_calls_done_per_time(elevator_calls):
    calls_done_per_time = {}
    for elevator_call in elevator_calls:
        if elevator_call.call_status == CallStatus.done:
            if elevator_call.closed_at in calls_done_per_time:
                calls_done_per_time[elevator_call.closed_at] += 1
            else:
                calls_done_per_time[elevator_call.closed_at] = 1

    ordered = collections.OrderedDict(sorted(calls_done_per_time.items()))

    plt.plot(ordered.keys(), ordered.values())
    plt.xlabel('time')
    plt.ylabel('calls done')
    plt.show()
