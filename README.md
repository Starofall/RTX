# Real-Time Experimentation (RTX)

![Banner](https://raw.githubusercontent.com/Starofall/RTX/master/banner.PNG)


### Description
Real-Time Experimentation (RTX) tool allows for self-adaptation based on analysis of real time (streaming) data.
RTX is particularly useful in analyzing operational data in a Big Data environement.


### Minimal Setup
* Download the RTX code
* Run `python setup.py install` to download all dependencies 
* To run example experiments, first install [CrowdNav](https://github.com/Starofall/CrowdNav)
* To use Spark as a PreProcessor you also need to install Spark and set SPARK_HOME

### Abstractions

RTX has the following abstractions that can be implemented for any given service:
* PreProcessor - To handle Big Data volumes of data, this is used to reduce the volume
    * Example: Spark   
* DataProviders - A source of data to be used in an experiment
    * Example: KafkaDataProvider, HTTPRequestDataProvider
* ChangeProviders - Communicates experiment knobs/variables to the target system
    * Example: KafkaChangeProvider, HTTPRequestChangeProvider
* ExecutionStrategy - Define the process of an experiment
    * Example: Sequential, Gauss-Process-Self-Optimizing, Linear 
* ExperimentDefinition - A experiment is defined in a python file 
    * See `./experiment-specification/experiment.py`

### Supported execution strategies

* ExperimentsSeq - Runs a list of experiments one after another
    ```
    experiments_seq = [
        ...
        {
            "ignore_first_n_results": 100,
            "sample_size": 100,
            "knobs": {
                "exploration_percentage": 0.0
            }
        }
        ...
    ]
    ```


* SelfOptimizer - Runs multiple experiments and tries to find the best value for the knobs
    ```
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
            "max_speed_and_length_factor": [0.5, 1.5],
            "average_edge_duration_factor": [0.5, 1.5],
        }
    }
    ```
    
* StepExplorer - Goes through the ranges in steps (useful for graphs/heatmaps)
    ```
    step_explorer = {
        # If new changes are not instantly visible, we want to ignore some results after state changes
        "ignore_first_n_results": 10,
        # How many samples of data to receive for one run
        "sample_size": 10,
        # The variables to modify
        "knobs": {
            # defines a [from-to] interval and step
            "exploration_percentage": ([0.0, 0.2], 0.1),
            "freshness_cut_off_value": ([100, 400], 100)
        }
    }
    ```