# Example for using HTTP (with CrowdNav)
#
# Start the RTX test web service first
name = "Example-HTTP-Step"

execution_strategy = {
    "ignore_first_n_results": 0,
    "sample_size": 100,
    "type": "step_explorer",
    "knobs": {
        "x": ([-4.0, 4.0], 0.8),
        "y": ([-10.0, 10.0], 1.2)
    }
}


def primary_data_reducer(state, newData):
    cnt = state["count"]
    state["avg_result"] = (state["avg_result"] * cnt + newData["result"]) / (cnt + 1)
    state["count"] = cnt + 1
    return state


primary_data_provider = {
    "type": "http_request",
    "url": "http://localhost:3000",
    "serializer": "JSON",
    "data_reducer": primary_data_reducer
}

change_provider = {
    "type": "http_request",
    "url": "http://localhost:3000",
    "serializer": "JSON",
}

secondary_data_providers = []


def evaluator(resultState):
    return resultState["avg_result"]


def state_initializer(state):
    state["count"] = 0
    state["avg_result"] = 0
    return state


def change_event_creator(variables):
    return variables


pre_processors = []
