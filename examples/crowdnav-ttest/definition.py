# Simple sequantial run of knob values
import os
import pandas as pd
from scipy import stats
import itertools

name = "CrowdNav-TTest"

exp_count =0


execution_strategy = {
    "ignore_first_n_results": 1000,
    "sample_size": 10000,
    "type": "sequential",
    "knobs": [
        {"route_random_sigma": 0.0},
        {"route_random_sigma": 0.2},
        {"route_random_sigma": 0.4},
        {"route_random_sigma": 0.6},
    ]
}
knobs_list = []
for i in execution_strategy["knobs"]:
    knobs_list.append(i["route_random_sigma"])

def primary_data_reducer(state, newData, wf):

    cnt = state["count"]
    state["overhead"] = newData["overhead"]
    state["count"] = cnt + 1
    state["file"].write(str(state["count"]) + "," + str(state["overhead"]) + "\n" )
    return state


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


def evaluator(resultState, wf):
    resultState["file"].close()

    global exp_count
    iter_list = list(itertools.combinations(range(1,(exp_count + 1), 1),2))
    result = []
    for comb in  [i for i in iter_list if i[1] == exp_count]:
        df1 = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/exp" + str(comb[0])+ ".txt")
        df2 = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/exp" + str(comb[1])+ ".txt")
        result.append({(knobs_list[comb[0]-1],knobs_list[comb[1]-1]) : stats.ttest_ind(df1["overhead"],df2["overhead"])[1]})
    return result


def state_initializer(state, wf):
    global exp_count
    exp_count += 1

    state["count"] = 0
    state["overhead"] = 0

    state["file"] =  open(os.path.dirname(os.path.realpath(__file__)) + '/exp'+str(exp_count)+'.txt','w')
    state["file"].write("count,overhead\n")
    return state
