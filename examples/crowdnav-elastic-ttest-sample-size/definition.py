name = "CrowdNav-Sequential"
analysis = "t-test-sample-estimation"
alpha = 0.05
power = 0.8
mean_diff = 0.1


def evaluator(resultState, wf):
    return 0


def workflow_evaluator(wf):

    data1 = wf.db.get_data_points(wf.analysis_id, 0)
    data2 = wf.db.get_data_points(wf.analysis_id, 1)

    x1 = [d["overhead"] for d in data1]
    x2 = [d["overhead"] for d in data2]

    pooled_std = wf.math.sqrt((wf.np.var(x1) + wf.np.var(x2)) / 2)

    effect_size = mean_diff / pooled_std

    sample_size = wf.statpower.tt_ind_solve_power(effect_size=effect_size, nobs1=None, alpha=alpha, power=power, alternative='two-sided')

    result = {"effect_size": effect_size, "sample_size": wf.math.floor(sample_size), "alpha": alpha, "power": power, "mean_diff": mean_diff, "pooled_std": pooled_std}
    wf.db.save_analysis_result(wf.analysis_id, result)
    print result

    return True

def state_initializer(state, wf):
    state["data_points"] = 0
    return state

def primary_data_reducer(state, newData, wf):
    wf.db.save_data_point(wf.experimentCounter, wf.current_knobs, newData, state["data_points"], wf.analysis_id)
    state["data_points"] += 1
    return state


execution_strategy = {
    "ignore_first_n_results": 0,
    "sample_size": 2,
    "type": "sequential",
    "knobs": [
        {"route_random_sigma": 0.0},
        {"route_random_sigma": 0.2}
    ]
}

primary_data_provider = {
    "type": "kafka_consumer",
    "kafka_uri": "kafka:9092",
    "topic": "crowd-nav-trips",
    "serializer": "JSON",
    "data_reducer": primary_data_reducer
}

change_provider = {
    "type": "kafka_producer",
    "kafka_uri": "kafka:9092",
    "topic": "crowd-nav-commands",
    "serializer": "JSON",
}