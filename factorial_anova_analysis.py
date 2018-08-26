from rtxlib.rtx_run import setup_database, db
from analysis_lib.factorial_tests import FactorialAnova
from parallel import get_experiment_list
from statsmodels.graphics.factorplots import interaction_plot

strategy_knobs = {
    "route_random_sigma": ([0.0, 0.3], 0.3),
    "exploration_percentage": ([0.0, 0.3], 0.3),
    "max_speed_and_length_factor": ([1.0, 2.5], 1.5),
    "average_edge_duration_factor": ([1.0, 2.5], 1.5),
    "freshness_update_factor": ([5, 20], 15),
    "freshness_cut_off_value": ([100, 700], 600),
    "re_route_every_ticks": ([10, 70], 60),
}


def save_dict_to_file(all_complaints, file_name):
    import pickle
    pickle_out = open(file_name,"wb")
    pickle.dump(all_complaints, pickle_out)
    pickle_out.close()
    print "data saved to file " + file_name


def retrieve_dict_from_file(file_name):
    import pickle
    import os.path
    pickle_in = open(file_name,"rb")
    # pickle_in = open(os.path.join('results-CrowdNav', 'raw data', file_name),"rb")
    all_complaints = pickle.load(pickle_in)
    print "data retrieved from file " + file_name
    return all_complaints


def get_raw_data(index, from_server):
    file_name = index + ".pickle"
    if from_server:
        setup_database(index)
        res = db().get_all_data_points()
        save_dict_to_file(res, file_name)
    else:
        res = retrieve_dict_from_file(file_name)
    return res


def create_experiment_configuration(knobs_keys, knobs_values):
    exp_conf = {}
    for i in range(len(knobs_keys)):
        exp_conf[knobs_keys[i]] = knobs_values[i]
    return exp_conf


def get_data_and_knobs(index, strategy_knobs, from_server):
    results = get_raw_data(index, from_server)

    exp_list = get_experiment_list("step_explorer", strategy_knobs)

    cnt = 0
    data = {}
    knobs = {}

    print "~~~~~~~~~"
    print index
    print "~~~~~~~~~"

    for knob_values in exp_list:
        exp_conf = create_experiment_configuration(strategy_knobs.keys(), knob_values)

        # exp_conf1 = exp_conf.copy()
        # exp_conf1["route_random_sigma"] = 0.0
        # exp_conf2 = exp_conf.copy()
        # exp_conf2["route_random_sigma"] = 0.3

        # res = [r for r in results if r[1]==exp_conf1 or r[1]==exp_conf2]
        res = [r for r in results if r[1]==exp_conf]
        data[cnt] = [r[0] for r in res]
        knobs[cnt] = [r[1] for r in res]
        # print exp_conf
        # print "Data: " + str(len(data[cnt]))
        cnt += 1
    print "========="

    return data, knobs, cnt


def make_data_smaller(index, strategy_knobs):

    results = get_raw_data(index, False, 10000)

    exp_list = get_experiment_list("step_explorer", strategy_knobs)

    print "~~~~~~~~~"
    print index
    print "~~~~~~~~~"

    new_results = []
    for knob_values in exp_list:
        exp_conf = create_experiment_configuration(strategy_knobs.keys(), knob_values)
        res = [r for r in results if r[1]==exp_conf]
        print exp_conf
        print "res: " + str(len(res))
        new_res = res[:1000]
        print "new_res: " + str(len(new_res))
        new_results += new_res
    print "========="
    print "new_results: " + str(len(new_results))

    file_name = index + "-1000.pickle"
    save_dict_to_file(new_results, file_name)


if __name__ == '__main__':

    # index = "rtxfactorial1"      # 750 cars, 750 smart cars
    # index = "rtxfactorial350"    # 750 cars, 350 smart cars
    index = "rtxfactorial350350" # 350 cars, 350 smart cars

    data, knobs, exp_count = get_data_and_knobs(index, strategy_knobs, True, 1000)
    print "exp_count: " + str(exp_count)

    # make_data_smaller(index, strategy_knobs)


    fake_run_id = "123456"
    y_key = 'overhead'

    aov_table = FactorialAnova(fake_run_id, y_key, strategy_knobs.keys(), exp_count).start(data, knobs)
    save_dict_to_file(aov_table, index + "_res.pickle")
    print "-------------"





    # if __name__ == '__main__':
    # index = "rtxfactorial1"
    # aov_table = retrieve_dict_from_file(index + "_res.pickle")
    # aov_table = aov_table.sort_values(by='PR(>F)', ascending=True)
    # probabilities = aov_table["PR(>F)"]
    #
    # significant_probs =  probabilities[probabilities < 0.01]
    #
    # print significant_probs
    #
    # print "Evaluated " + str(len(probabilities)) + " out of which " + str(len(significant_probs)) + " were found significant."

    # fig = interaction_plot(data.dose, data.supp, data.len, ms=10)

    # knob_names = [
    #     "route_random_sigma",
    #     "exploration_percentage",
    #     "max_speed_and_length_factor",
    #     "average_edge_duration_factor",
    #     "freshness_update_factor",
    #     "freshness_cut_off_value",
    #     "re_route_every_ticks",
    # ]
    #
    # knob_values = [
    #     [0, 0.3],          # route_random_sigma
    #     [0, 0.3],          # exploration_percentage
    #     [1, 2.5],          # max_speed_and_length_factor
    #     [1, 2.5],          # average_edge_duration_factor
    #     [5, 20],           # freshness_update_factor
    #     [100, 700],        # freshness_cut_off_value
    #     [10, 70]           # re_route_every_ticks"
    # ]
    #
    # default_dict = {
    #     "route_random_sigma" : 0,
    #     "exploration_percentage": 0,
    #     "max_speed_and_length_factor": 1,
    #     "average_edge_duration_factor": 1,
    #     "freshness_update_factor": 5,
    #     "freshness_cut_off_value": 100,
    #     "re_route_every_ticks": 10
    # }

    # def get_knob_keys():
    #     knob_keys = []
    #     knob_name_ind = 0
    #     for knob_name in knob_names:
    #         for knob_value in knob_values[knob_name_ind]:
    #             knob_key = {}
    #             knob_key[knob_name] = knob_value
    #             knob_keys.append(knob_key)
    #         knob_name_ind += 1
    #     return knob_keys

    # def get_full_knobs_dict(retrieved_dict):
    #     full_dict = {}
    #     for knob_name in knob_names:
    #         if knob_name in retrieved_dict:
    #             full_dict[knob_name] = retrieved_dict[knob_name]
    #         else:
    #             full_dict[knob_name] = default_dict[knob_name]
    #     return full_dict