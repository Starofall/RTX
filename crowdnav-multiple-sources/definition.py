# The name of this workflow
name = "CrowdNav-Step"

execution_strategy = {
    "type": "step_explorer",
    # If new changes are not instantly visible, we want to ignore some results after state changes
    "ignore_first_n_results": 10,
    # How many samples of data to receive for one run
    "sample_size": 20,
    # The variables to modify
    "knobs": {
        # defines a [from-to] interval and step
        # "exploration_percentage": ([0.0, 0.4], 0.1),
        "re_route_every_ticks": ([0, 6], 1)
    }
}

pre_processors = [
    # {
    #     # the type of the preprocessor
    #     "type": "spark",
    #     # currently we only support "local_jar"
    #     "submit_mode": "local_jar",
    #     # name of the spark jobs jar (located in the experiment's folder) - e.g. "assembly-1.0.jar"
    #     "job_file": "assembly-1.0.jar",
    #     # the class of the script to start - e.g. "crowdnav.Main"
    #     "job_class": "crowdnav.Main"
    # },
    # {
    #     # the type of the preprocessor
    #     "type": "spark",
    #     # currently we only support "local_jar"
    #     "submit_mode": "local_jar",
    #     # name of the spark jobs jar (located in the experiment's folder) - e.g. "assembly-1.0.jar"
    #     "job_file": "assembly-1.0.jar",
    #     # the class of the script to start - e.g. "crowdnav.Main"
    #     "job_class": "crowdnav.Main"
    # }
]


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


def routing_data_reducer(state, newData):
    cnt = state["routing_count"]
    state["routing_avg"] = (state["routing_avg"] * cnt + newData["duration"]) / (cnt + 1)
    state["routing_count"] = cnt + 1
    # if state["routing_count"] > 100 and state["routing_avg"] > 20:
    # raise StopIteration("routing got too exponsive")
    # raise RuntimeError("stop the whole workflow")
    return state


primary_data_provider = {
    "type": "kafka_consumer",
    "kafka_uri": "kafka:9092",
    "topic": "crowd-nav-trips",
    "serializer": "JSON",
    "data_reducer": primary_data_reducer
}

secondary_data_providers = [
    {
        "type": "kafka_consumer",
        "kafka_uri": "kafka:9092",
        "topic": "crowd-nav-performance",
        "serializer": "JSON",
        "data_reducer": performance_data_reducer
    },
    {
        "type": "kafka_consumer",
        "kafka_uri": "kafka:9092",
        "topic": "crowd-nav-routing",
        "serializer": "JSON",
        "data_reducer": routing_data_reducer
    }
]

change_provider = {
    "type": "kafka_producer",
    # Where we can connect to kafka - e.g. kafka:9092
    "kafka_uri": "kafka:9092",
    # The topic to listen to
    "topic": "crowd-nav-commands",
    # The serializer we want to use for kafka messages
    #   Currently only "JSON" is supported
    "serializer": "JSON",
}


def evaluator(resultState):
    return resultState["routing_avg"]


def state_initializer(state):
    state["count"] = 0
    state["avg_overhead"] = 0
    state["duration_avg"] = 0
    state["duration_count"] = 0
    state["routing_avg"] = 0
    state["routing_count"] = 0
    return state


def change_event_creator(variables):
    return variables

#
# # If we use ExecutionStrategy "self_optimizer" ->
# self_optimizer = {
#     # Currently only "gauss_process" is supported
#     "method": "",
#     # If new changes are not instantly visible, we want to ignore some results after state changes
#     "ignore_first_n_results": 1000,
#     # How many samples of data to receive for one run
#     "sample_size": 1000,
#     # The variables to modify
#     "knobs": {
#         # defines a [from-to] interval that will be used by the optimizer
#         "variable_name": [0.0, 1.0]
#     }
# }
#
# # If we use ExecutionStrategy "sequential" ->
# experiments_seq = [
#     {
#         # Variable that is changed in the process
#         "knobs": {
#             "variable_name": 0.0
#         },
#         # If new changes are not instantly visible, we want to ignore some results after state changes
#         "ignore_first_n_results": 1000,
#         # How many samples of data to receive for one run
#         "sample_size": 1000,
#     },
#     {
#         # Variable that is changed in the process
#         "knobs": {
#             "variable_name": 0.1
#         },
#         # If new changes are not instantly visible, we want to ignore some results after state changes
#         "ignore_first_n_results": 1000,
#         # How many samples of data to receive for one run
#         "sample_size": 1000,
#     }
# ]
#
# # If we use ExecutionStrategy "sequential" ->
# step_explorer = {
#     # If new changes are not instantly visible, we want to ignore some results after state changes
#     "ignore_first_n_results": 10,
#     # How many samples of data to receive for one run
#     "sample_size": 10,
#     # The variables to modify
#     "knobs": {
#         # defines a [from-to] interval and step
#         "variable_name": ([0.0, 0.4], 0.1),
#     }
# }
