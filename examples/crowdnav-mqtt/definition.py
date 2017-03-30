# Example for using MQTT (with CrowdNav)
#
# Starting MQTT (mosquitto) with docker
# docker run --name mqtt -d -p 1883:1883 -p 9001:9001 toke/mosquitto
#
name = "CrowdNav-MQTT"

execution_strategy = {
    "type": "step_explorer",
    "ignore_first_n_results": 1000,
    "sample_size": 1000,
    "knobs": {
        "total_car_counter": ([200, 1000], 200)
    }
}


def primary_data_reducer(state, newData, wf):
    cnt = state["count"]
    state["avg_overhead"] = (state["avg_overhead"] * cnt + newData["overhead"]) / (cnt + 1)
    state["count"] = cnt + 1
    return state


def performance_data_reducer(state, newData, wf):
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


def evaluator(resultState, wf):
    return resultState["avg_overhead"]


def state_initializer(state, wf):
    state["count"] = 0
    state["avg_overhead"] = 0
    state["duration_avg"] = 0
    state["duration_count"] = 0
    return state
