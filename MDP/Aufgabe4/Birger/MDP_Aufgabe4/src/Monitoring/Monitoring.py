import collections
import copy

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

    plt.figure(1)
    plt.plot(ordered.keys(), ordered.values())
    plt.xlabel('time')
    plt.ylabel('calls done')
    plt.draw()


def plot_waitingtime_per_time():
    waitingtime_per_time = {}
    for timestamp, calls in calls_per_time.iteritems():
        waitingtime_per_time[timestamp] = get_average_waitingtime_by_calls(calls)

    ordered = collections.OrderedDict(sorted(waitingtime_per_time.items()))

    plt.figure(2)
    plt.subplot(212)
    plt.plot(ordered.keys(), ordered.values())
    plt.xlabel('time')
    plt.ylabel('average waitingtime')
    plt.draw()


def plot_takeawaytime_per_time():
    takeawaytime_per_time = {}
    for timestamp, calls in calls_per_time.iteritems():
        takeawaytime_per_time[timestamp] = get_average_takeawaytime_by_calls(calls)

    ordered = collections.OrderedDict(sorted(takeawaytime_per_time.items()))

    plt.figure(2)
    plt.subplot(211)
    plt.plot(ordered.keys(), ordered.values())
    plt.xlabel('time')
    plt.ylabel('average takeawaytime')
    plt.draw()


def show_plots():
    plt.show()


def get_average_waitingtime_by_calls(calls):
    result = 0
    accu = 0

    if len(calls):
        for call in calls:
            if call.call_status == statuses.CallStatus.done or call.call_status == statuses.CallStatus.takeaway:
                accu += (call.takenup_at - call.open_at)
        result = accu / len(calls)
    return result


def get_average_takeawaytime_by_calls(calls):
    result = 0
    accu = 0

    if len(calls):
        for call in calls:
            if call.call_status == statuses.CallStatus.done:
                accu += (call.closed_at - call.takenup_at)
        result = accu / len(calls)
    return result


def collect_calls_on_time(timestamp, all_calls):
    temp_calls = []
    for call in all_calls:
        temp_calls.append(copy.deepcopy(call))
    calls_per_time[timestamp] = temp_calls
