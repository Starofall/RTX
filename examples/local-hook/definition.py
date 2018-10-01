name = "Local Hook"

execution_strategy = {
    "ignore_first_n_results": 0,
    "sample_size": 1,
    "type": "step_explorer",
    "knobs": {
        "a": ([1.0, 100.0], 30.0),
        "b": ([1.0, 100.0], 30.0)
    }
}


def evaluator(resultState, wf):
    return resultState["result"]


def state_initializer(state, wf):
    state["result"] = 999999999
    return state


def primary_data_reducer(state, newData, wf):
    state["result"] = newData["result"]
    return state


currentConfiguration = {
    "a": 0,
    "b": 0
}


def setParameterHook(params):
    currentConfiguration.update(params)


def getResultsHook():
    a = currentConfiguration["a"]
    b = currentConfiguration["b"]
    return {
        "result": a*b
    }


change_provider = {
    "type": "local_hook",
    "setParameterHook": setParameterHook,
}

primary_data_provider = {
    "type": "local_hook",
    "data_reducer": primary_data_reducer,
    "getResultsHook": getResultsHook
}
