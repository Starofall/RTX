# Example for using HTTP (with CrowdNav)
#
# Start the RTX test web service first
name = "Example-HTTP-Step"

execution_strategy = {
    # ignoring does not make sense, as changes happen instantly
    "ignore_first_n_results": 0,
    # we sample the data to minimize randomness in the collected values
    "sample_size": 100,
    # we want to see the hole steps
    "type": "step_explorer",
    # Here we look at x (from -4 to 4 in steps of 0.8) and y (from -10 to 10 in steps of 1.2)
    "knobs": {
        "x": ([-4.0, 4.0], 0.8),
        "y": ([-10.0, 10.0], 1.2)
    }
}


def primary_data_reducer(state, newData, wf):
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


def evaluator(resultState, wf):
    return resultState["avg_result"]


def state_initializer(state, wf):
    state["count"] = 0
    state["avg_result"] = 0
    return state
