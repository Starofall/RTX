from colorama import Fore
from rtxlib import info

name = "Traffic-A9"

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

    if newData["id"].startswith("loop0500") :
        cnt = state["occupancies_count"]["lower"]
        state["occupancies_avg"]["lower"] = (state["occupancies_avg"]["lower"] * cnt + newData["occupancy"]) / (cnt + 1)
        state["occupancies_count"]["lower"] = cnt + 1

    else:
        cnt = state["occupancies_count"]["upper"]
        state["occupancies_avg"]["upper"] = (state["occupancies_avg"]["upper"] * cnt + newData["occupancy"]) / (cnt + 1)
        state["occupancies_count"]["upper"] = cnt + 1

    return state

def speeds_data_reducer(state, newData, wf):
    cnt = state["speeds_count"]
    state["speeds_avg"] = (state["speeds_avg"] * cnt + newData["speed"]) / (cnt + 1)
    state["speeds_count"] = cnt + 1
    return state

def evaluator(resultState, wf):
    if resultState["occupancies_avg"]["upper"] > 2.5 and resultState["occupancies_avg"]["lower"] > 2.5:
        # open hard shoulder
        info("Command to open hard shoulder sent...", Fore.CYAN)
        wf.change_provider.applyChange({"hard_shoulder": 1})
    if resultState["occupancies_avg"]["upper"] < 1.5 and resultState["occupancies_avg"]["lower"] < 1.5:
        # close hard shoulder
        info("Command to close hard shoulder sent...", Fore.CYAN)
        wf.change_provider.applyChange({"hard_shoulder": 0})
    return resultState["occupancies_avg"]

def state_initializer(state, wf):
    state["tick_count"] = 0
    state["occupancies_avg"] = dict()
    state["occupancies_avg"]["lower"] = 0
    state["occupancies_avg"]["upper"] = 0
    state["occupancies_count"] = dict()
    state["occupancies_count"]["lower"] = 0
    state["occupancies_count"]["upper"] = 0
    state["speeds_avg"] = 0
    state["speeds_count"] = 0
    return state

def change_event_creator(variables, wf):
    return variables

primary_data_provider = {
    "type": "interval",
    "seconds": 0.5,
    "data_reducer": ticks_data_reducer
}

# primary_data_provider = {
#     "type": "kafka_consumer",
#     "kafka_uri": "kafka:9092",
#     "topic": "ticks",
#     "serializer": "JSON",
#     "data_reducer": ticks_data_reducer
# }

secondary_data_providers = [
    {
        "type": "kafka_consumer",
        "kafka_uri": "kafka:9092",
        "topic": "occupancies",
        "serializer": "JSON",
        "data_reducer": occupancies_data_reducer
    },
    {
        "type": "kafka_consumer",
        "kafka_uri": "kafka:9092",
        "topic": "speeds",
        "serializer": "JSON",
        "data_reducer": speeds_data_reducer
    }
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