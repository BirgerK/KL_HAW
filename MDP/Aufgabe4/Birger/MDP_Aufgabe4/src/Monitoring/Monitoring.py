import collections

import matplotlib.pyplot as plt

import Simulation.Statuses as statuses

calls_per_time = {}


def plot_calls_done_per_time():
    calls_done_per_time = {}
    for timestamp, calls in calls_per_time.iteritems():
        calls_done = 0
        for call in calls:
            if call.call_status == statuses.CallStatus.done:
                calls_done += 1
        calls_done_per_time[timestamp] = calls_done

    ordered = collections.OrderedDict(sorted(calls_done_per_time.items()))

    plt.plot(ordered.keys(), ordered.values())
    plt.xlabel('time')
    plt.ylabel('calls done')
    plt.show()


def plot_waitingtime_per_time():
    waitingtime_per_time = {}
    for timestamp, calls in calls_per_time.iteritems():
        waitingtime_per_time[timestamp] = get_average_waitingtime_by_calls(calls)

    ordered = collections.OrderedDict(sorted(waitingtime_per_time.items()))

    plt.plot(ordered.keys(), ordered.values())
    plt.xlabel('time')
    plt.ylabel('average waitingtime')
    plt.show()


def get_average_waitingtime_by_calls(calls):
    result = 0
    accu = 0

    if len(calls):
        for call in calls:
            if call.call_status == statuses.CallStatus.done or call.call_status == statuses.CallStatus.takeaway:
                accu += (call.takenup_at - call.opened_at)
        result = accu / len(calls)
    return result


def collect_calls_on_time(timestamp, all_calls):
    calls_per_time[timestamp] = list(all_calls)
