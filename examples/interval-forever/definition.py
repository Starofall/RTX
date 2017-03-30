# Example for using HTTP (with CrowdNav)
#
# Start the RTX test web service first
name = "Example-HTTP-Gauss"

execution_strategy = {
    "ignore_first_n_results": 0,
    "sample_size": 20,
    "type": "forever"
}


def primary_data_reducer(state, newData,wf):
    state["count"] += 1
    return state


primary_data_provider = {
    "type": "interval",
    "seconds": 0.1,
    "data_reducer": primary_data_reducer
}

change_provider = {
    "type": "dummy"
}


def evaluator(resultState,wf):
    return resultState["count"]


def state_initializer(state,wf):
    state["count"] = 0
    return state
