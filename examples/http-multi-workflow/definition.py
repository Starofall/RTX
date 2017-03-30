# Example for using multi workflow
#
# Start the RTX test web service first
name = "Example-HTTP-Gauss"

execution_strategy = {
    "ignore_first_n_results": 0,
    "sample_size": 100,
    "type": "uncorrelated_self_optimizer",
    "optimizer_method": "gauss",
    "optimizer_iterations": 20,
    "optimizer_random_starts": 10,
    "knobs": {
        "x": (-4.0, 4.0),
        "y": (-10.0, 10.0)
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


def change_event_creator(variables, wf):
    return variables
