# Example for using MQTT (with CrowdNav)
#
# Starting MQTT (mosquitto) with docker
# docker run --name mqtt -d -p 1883:1883 -p 9001:9001 toke/mosquitto
name = "Example-MQTT"

execution_strategy = {
    "type": "step_explorer",
    "ignore_first_n_results": 100,
    "sample_size": 100,
    "knobs": {
        # "nothing": ([0, 10], 1)
        "total_car_counter": ([100,1500], 100)
    }
}


def primary_data_reducer(state, newData):
    cnt = state["count"]
    state["avg_overhead"] = (state["avg_overhead"] * cnt + newData["overhead"]) / (cnt + 1)
    state["count"] = cnt + 1
    return state


def performance_data_reducer(state, newData):
    cnt = state["duration_count"]
    state["duration_avg"] = (state["duration_avg"] * cnt + newData["duration"]) / (cnt + 1)
    state["duration_count"] = cnt + 1
    return state


primary_data_provider = {
    "type": "mqtt_listener",
    "host": "localhost",
    "port": "1883",
    "topic": "crowd-nav-trips",
    "serializer": "JSON",
    "data_reducer": primary_data_reducer
}

secondary_data_providers = [{
    "type": "mqtt_listener",
    "host": "localhost",
    "port": "1883",
    "topic": "crowd-nav-performance",
    "serializer": "JSON",
    "data_reducer": performance_data_reducer
}]

change_provider = {
    "type": "mqtt_publisher",
    "host": "localhost",
    "port": "1883",
    "topic": "crowd-nav-commands",
    "serializer": "JSON",
}


def evaluator(resultState):
    return resultState["avg_overhead"]


def state_initializer(state):
    state["count"] = 0
    state["avg_overhead"] = 0
    state["duration_avg"] = 0
    state["duration_count"] = 0
    return state


def change_event_creator(variables):
    return variables


pre_processors = []
