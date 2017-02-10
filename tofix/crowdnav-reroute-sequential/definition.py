# for documentation see file /experiment-specification/definition.py

name = "CrowdNav-Sequential"


def evaluator(resultState):
    return resultState["avg_overhead"]


def initial_state(state):
    state["count"] = 0
    state["avg_overhead"] = 0
    return state


def data_reducer(state, newData):
    cnt = state["count"]
    state["avg_overhead"] = (state["avg_overhead"] * cnt + newData["overhead"]) / (cnt + 1)
    state["count"] = cnt + 1
    return state


def change_event_creator(variables):
    return variables


system = {
    "execution_strategy": "sequential",
    "pre_processor": "none",
    "data_provider": "kafka_consumer",
    "change_provider": "kafka_producer",
    "state_initializer": initial_state,
    "data_reducer": data_reducer,
    "evaluator": evaluator,
    "change_event_creator": change_event_creator
}

configuration = {
    "kafka_producer": {
        "kafka_uri": "kafka:9092",
        "topic": "crowd-nav-commands",
        "serializer": "JSON",
    },
    "kafka_consumer": {
        "kafka_uri": "kafka:9092",
        "topic": "crowd-nav-trips",
        "serializer": "JSON",
    }
}

experiments_seq = [
    {
        "ignore_first_n_results": 500,
        "sample_size": 3000,
        "knobs": {
            "re_route_every_ticks": 0
        }
    },
    {
        "ignore_first_n_results": 500,
        "sample_size": 3000,
        "knobs": {
            "re_route_every_ticks": 5
        }
    },
    {
        "ignore_first_n_results": 500,
        "sample_size": 3000,
        "knobs": {
            "re_route_every_ticks": 10
        }
    },
    {
        "ignore_first_n_results": 500,
        "sample_size": 3000,
        "knobs": {
            "re_route_every_ticks": 15
        }
    },
    {
        "ignore_first_n_results": 500,
        "sample_size": 3000,
        "knobs": {
            "re_route_every_ticks": 20
        }
    }
]
