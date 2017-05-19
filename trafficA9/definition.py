from __future__ import division
from colorama import Fore
from rtxlib import info

name = "Traffic-A9"

overall_ticks = 0

execution_strategy = {
    # the strategy runs in a loop forever
    "type": "forever",
    # If new changes are not instantly visible, we want to ignore some results after state changes
    "ignore_first_n_results": 0,
    # How many samples of data to receive for one run
    "sample_size": 60,
}

def ticks_data_reducer(state, newData, wf):
    state["tick_count"] += 1
    return state

def occupancies_data_reducer(state, newData, wf):

    if newData["position"] == 500 :
        state["occurrences"]["lower"] += newData["occupancy"]
        state["occurrences_count"]["lower"] += 1

        # print newData["occupancy"]
        # cnt = state["occupancies_count"]["lower"]
        # state["occupancies_avg"]["lower"] = (state["occupancies_avg"]["lower"] * cnt + newData["occupancy"]) / (cnt + 1)
        # state["occupancies_count"]["lower"] = cnt + 1

    # else:
    #     cnt = state["occupancies_count"]["upper"]
    #     state["occupancies_avg"]["upper"] = (state["occupancies_avg"]["upper"] * cnt + newData["occupancy"]) / (cnt + 1)
    #     state["occupancies_count"]["upper"] = cnt + 1

    return state

def speeds_data_reducer(state, newData, wf):
    cnt = state["speeds_count"]
    state["speeds_avg"] = (state["speeds_avg"] * cnt + newData["speed"]) / (cnt + 1)
    state["speeds_count"] = cnt + 1
    return state

def evaluator(resultState, wf):
    occurrences = resultState["occurrences"]["lower"]
    print occurrences
    occurrences_count = resultState["occurrences_count"]["lower"]
    print occurrences_count
    product = occurrences / occurrences_count
    print product
    tick_count = resultState["tick_count"]
    print tick_count
    if product > 2.5:
            # and resultState["occupancies_avg"]["upper"] > 2.5:
        info("Command to open hard shoulder sent...", Fore.CYAN)
        wf.change_provider["instance"].applyChange({"hard_shoulder": 1})
        hard_shoulder_open = True
    if product < 1.5:
            # and resultState["occupancies_avg"]["upper"] < 1.5:
        info("Command to close hard shoulder sent...", Fore.CYAN)
        wf.change_provider["instance"].applyChange({"hard_shoulder": 0})
        hard_shoulder_open = False
    global overall_ticks
    overall_ticks = overall_ticks + tick_count
    return [overall_ticks,product]

def state_initializer(state, wf):
    state["overall_tick_count"] = 0
    state["tick_count"] = 0
    state["occurrences"] = dict()
    state["occurrences"]["lower"] = 0
    state["occurrences"]["upper"] = 0
    state["occurrences_count"] = dict()
    state["occurrences_count"]["lower"] = 0
    state["occurrences_count"]["upper"] = 0
    state["speeds_avg"] = 0
    state["speeds_count"] = 0
    return state

def change_event_creator(variables, wf):
    return variables

# primary_data_provider = {
#     "type": "interval",
#     "seconds": 0.5,
#     "data_reducer": ticks_data_reducer
# }

primary_data_provider = {
    "type": "kafka_consumer",
    "kafka_uri": "kafka:9092",
    "topic": "ticks",
    "serializer": "JSON",
    "data_reducer": ticks_data_reducer
}

secondary_data_providers = [
    {
        "type": "kafka_consumer",
        "kafka_uri": "kafka:9092",
        "topic": "occupancies",
        "serializer": "JSON",
        "data_reducer": occupancies_data_reducer
    },
    # {
    #     "type": "kafka_consumer",
    #     "kafka_uri": "kafka:9092",
    #     "topic": "speeds",
    #     "serializer": "JSON",
    #     "data_reducer": speeds_data_reducer
    # }
]

change_provider = {
    "type": "kafka_producer",
    # Where we can connect to kafka - e.g. kafka:9092
    "kafka_uri": "kafka:9092",
    # The topic to listen to
    "topic": "shoulder-control",
    # The serializer we want to use for kafka messages
    #   Currently only "JSON" is supported
    "serializer": "JSON",
}

pre_processors = []