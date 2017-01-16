# The name of this workflow
name = ""

# Defines the system settings of how we want to run this experiment
system = {

    # Defines how to run experiments
    # "sequential"    -> Runs a list of experiments in a sequential way
    #    requires a "experiments_seq" array
    # "self_optimizer" -> Runs a self adaptation algorithm to optimize values
    #    requires a "self_optimizer" object in the definition
    "execution_strategy": "",

    # We can install a preprocessor like Spark to reduce data volume
    # "spark" -> Submits a preprocessor to spark to reduce the message volume
    #    requires a "spark" element in the configuration section
    # "none"  -> We directly connect to the data source and do not use a preprocessor
    "pre_processor": "",

    # What provider we use to get data from the running experiments
    # "kafka_consumer" -> Gathers data through listening to a kafka topic
    #    requires a "kafkaConsumer" element in the configuration section
    # "mqtt_listener" -> Gathers data from a MQTT queue
    #    Not yet implemented
    # "http_data_requests" -> Gathers data from doing active http requests to the system
    #    Not yet implemented
    "data_provider": "",

    # What provider we use to change the running experiment
    # "kafka_producer" -> Doing changes by pushing to kafka
    #    requires a "kafkaProducer" element in the configuration section
    # "mqtt_publisher" -> Doing changes by pushing to mqtt
    #    Not yet implemented
    # "http_change_requests" -> Doing changes by calling a http interface
    #    Not yet implemented
    "change_provider": "",

    # Initializes a new state for an experiment
    #   definition: (empty_dict) => init_state
    "state_initializer": lambda empty_dict: {},

    # All incoming streaming data are reduced
    #   definition: (old_state,new_data) => new_state
    "data_reducer": lambda old_state, new_data: {},

    # The evaluation function that evaluates this experiment
    # Auto optimizing is trying to minimize this value
    #   definition: (result_state) => float
    "evaluator": lambda result_state: 0.0,

    # As variables change in the run, this function is used to generate the input
    # of the change provider to apply the new variable.
    #   definition: (variables) => input_for_change_provider
    "change_event_creator": lambda result_state: {}
}

# Defines the settings for the modules used in the workflow
configuration = {
    # If we use the Spark preprocessor, we have to define this sparkConfig
    "spark": {
        # currently we only support "local_jar"
        "submit_mode": "local_jar",
        # name of the spark jobs jar (located in the experiment's folder)
        "job_file": "CrowdNavSpark-assembly-1.0.jar",
        # the class of the script to start
        "job_class": "crowdnav.Main"
    },
    # If we use KafkaProducer as a ChangeProvider, we have to define this kafkaProducerConfig
    "kafka_producer": {
        # Where we can connect to kafka
        "kafka_uri": "sparfka:9092",
        # The topic to listen to
        "topic": "crowd-nav-commands",
        # The serializer we want to use for kafka messages
        #   Currently only "JSON" is supported
        "serializer": "JSON",
    },
    # If we use KafkaConsumer as a DataProvider, we have to define this kafkaConsumerConfig
    "kafka_consumer": {
        # Where we can connect to kafka
        "kafka_uri": "sparfka:9092",
        # The topic to listen to
        "topic": "crowd-nav-trips",
        # The serializer we want to use for kafka messages
        #   Currently only "JSON" is supported
        "serializer": "JSON",
    },
}

# If we use ExecutionStrategy "self_optimizer" ->
self_optimizer = {
    # Currently only Gauss Process
    "method": "gauss_process",
    # If new changes are not instantly visible, we want to ignore some results after state changes
    "ignore_first_n_results": 1000,
    # How many samples of data to receive for one run
    "sample_size": 1000,
    # The variables to modify
    "knobs": {
        # defines a [from-to] interval that will be used by the optimizer
        "victim_percentage": [0.0, 1.0]
    }
}

# If we use ExecutionStrategy "sequential" ->
experiments_seq = [
    {
        # Variable that is changed in the process
        "knobs": {
            "victim_percentage": 0.0
        },
        # If new changes are not instantly visible, we want to ignore some results after state changes
        "ignore_first_n_results": 1000,
        # How many samples of data to receive for one run
        "sample_size": 1000,
    },
    {
        # Variable that is changed in the process
        "knobs": {
            "victim_percentage": 0.1
        },
        # If new changes are not instantly visible, we want to ignore some results after state changes
        "ignore_first_n_results": 1000,
        # How many samples of data to receive for one run
        "sample_size": 1000,
    }
]
