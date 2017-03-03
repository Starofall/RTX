# The name of this workflow
name = ""

execution_strategy = {
    "type": "self_optimizer",
    # Currently only "gauss_process" is supported
    "method": "",
    # If new changes are not instantly visible, we want to ignore some results after state changes
    "ignore_first_n_results": 1000,
    # How many samples of data to receive for one run
    "sample_size": 1000,
    # The variables to modify
    "knobs": {
        # defines a [from-to] interval that will be used by the optimizer
        "variable_name": [0.0, 1.0]
    }
}

pre_processors = [
    {
        # the type of the preprocessor
        "type": "spark",
        # currently we only support "local_jar"
        "submit_mode": "",
        # name of the spark jobs jar (located in the experiment's folder) - e.g. "assembly-1.0.jar"
        "job_file": "",
        # the class of the script to start - e.g. "crowdnav.Main"
        "job_class": ""
    }
]

primary_data_provider = {
    "type": "kafka_consumer",
    "kafka_uri": "",
    "topic": "",
    "serializer": "",
    "data_reducer": lambda old_state, new_data: {},
}

secondary_data_providers = [
    {
        "type": "kafka_consumer",
        "kafka_uri": "",
        "topic": "",
        "serializer": "",
        "data_reducer": lambda old_state, new_data: {},
    }
]

change_provider = {
    "type": "kafka_producer",
    # Where we can connect to kafka - e.g. kafka:9092
    "kafka_uri": "",
    # The topic to listen to
    "topic": "",
    # The serializer we want to use for kafka messages
    #   Currently only "JSON" is supported
    "serializer": "",
}

state_initializer = lambda empty_dict: {},
evaluator = lambda result_state: 0.0,
change_event_creator = lambda result_state: {}

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
