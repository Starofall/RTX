# Simple sequantial run of knob values
import os
import pandas as pd
from scipy import stats
import itertools
import json

name = "CrowdNav-TTest"

exp_count =0
path_to_save = ""

execution_strategy = {
    "ignore_first_n_results": 10,
    "sample_size": 10,
    "type": "sequential",
    "knobs": [
        {"route_random_sigma": 0.0},
        {"route_random_sigma": 0.0},
        {"route_random_sigma": 0.0},
        {"route_random_sigma": 0.0},
        {"route_random_sigma": 0.0},
        {"route_random_sigma": 0.0},
        {"route_random_sigma": 0.0},
        {"route_random_sigma": 0.0},
        {"route_random_sigma": 0.0},
        {"route_random_sigma": 0.0},

    ],
    "sample_size_method": "test"
}
knobs_list = []
for i in execution_strategy["knobs"]:
    knobs_list.append(i.values()[0])

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
    global path_to_save
    global exp_count
    iter_list = list(itertools.combinations(range(1,(exp_count + 1), 1),2))
    result = []

    for comb in  [i for i in iter_list if i[1] == exp_count]:
        df1 = pd.read_csv(path_to_save + "/exp"+ str(comb[0])+ ".txt")
        df2 = pd.read_csv(path_to_save + "/exp" + str(comb[1])+ ".txt")
        result.append({(knobs_list[comb[0]-1],knobs_list[comb[1]-1]) : stats.ttest_ind(df1["overhead"],df2["overhead"])[1]})
    return result


def state_initializer(state, wf):
    global exp_count
    global  path_to_save
    exp_count += 1

    state["count"] = 0
    state["overhead"] = 0

    # Creatind the path of experiment session in order to save it
    i = 1
    while exp_count == 1:
        if (not os.path.isdir(os.path.dirname(os.path.realpath(__file__)) + "/saved_experiments/exp" + str(i)) ) :
            os.makedirs(os.path.dirname(os.path.realpath(__file__)) + "/saved_experiments/exp" + str(i))
            path_to_save = os.path.dirname(os.path.realpath(__file__)) + "/saved_experiments/exp" + str(i)
            break
        else:
            i +=1

    # Writing necessary information for experiment session
    with open(path_to_save + "/session_info.txt", "w") as text_file:
        json.dump(execution_strategy, text_file)
    state["file"] =  open(path_to_save + '/exp'+str(exp_count)+'.txt','w')
    state["file"].write("count,overhead\n")
    return state
