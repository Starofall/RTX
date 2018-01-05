from rtxlib.rtx_run import setup_database, db
from analysis_lib.factorial_tests import FactorialAnova

index = "rtx752"   # dual of 750
file_name = index + ".pickle"

knob_names = [
    "route_random_sigma",
    "exploration_percentage",
    # "max_speed_and_length_factor",
    # "average_edge_duration_factor",
    # "freshness_update_factor",
    # "freshness_cut_off_value",
    # "re_route_every_ticks",
]

knob_values = [
    [0, 0.2, 0.4, 0.6],   # route_random_sigma
    [0, 0.2, 0.4, 0.6],   # exploration_percentage
    [1, 1.5, 2, 2.5],     # max_speed_and_length_factor
    [1, 1.5, 2, 2.5],     # average_edge_duration_factor
    [5, 10, 15, 20],      # freshness_update_factor
    [100, 300, 500, 700], # freshness_cut_off_value
    [10, 30, 50, 70]      # re_route_every_ticks"
]

default_dict = {
    "route_random_sigma" : 0,
    "exploration_percentage": 0,
    "max_speed_and_length_factor": 1,
    "average_edge_duration_factor": 1,
    "freshness_update_factor": 10,
    "freshness_cut_off_value": 90,
    "re_route_every_ticks": 60
}


def get_knob_keys():
    knob_keys = []
    knob_name_ind = 0
    for knob_name in knob_names:
        for knob_value in knob_values[knob_name_ind]:
            knob_key = {}
            knob_key[knob_name] = knob_value
            knob_keys.append(knob_key)
        knob_name_ind += 1
    return knob_keys


def save_dict_to_file(all_complaints):
    import pickle
    pickle_out = open(file_name,"wb")
    pickle.dump(all_complaints, pickle_out)
    pickle_out.close()
    print "data saved to file " + file_name


def retrieve_dict_from_file():
    import pickle
    pickle_in = open(file_name,"rb")
    all_complaints = pickle.load(pickle_in)
    print "data retrieved from file " + file_name
    return all_complaints


def get_raw_data(from_server):
    if from_server:
        setup_database(index)
        res = db().get_all_data_points()
        save_dict_to_file(res)
        return res
    else:
        res = retrieve_dict_from_file()
        return res


def get_full_knobs_dict(retrieved_dict):
    full_dict = {}
    for knob_name in knob_names:
        if knob_name in retrieved_dict:
            full_dict[knob_name] = retrieved_dict[knob_name]
        else:
            full_dict[knob_name] = default_dict[knob_name]
    return full_dict

def get_data_and_knobs(from_server, sample_size):
    results = get_raw_data(from_server)

    data = {}
    knobs = {}

    cnt = 0
    print "~~~~~~~~~"
    print index
    print "~~~~~~~~~"
    for j in range(len(knob_names)):
        knob_name = knob_names[j]
        print knob_name
        print "---------"
        for i in knob_values[j]:
            res = [r for r in results if r[1].get(knob_name)==i]
            # ind = knob_name + "_" + str(i)
            data[cnt] = [r[0] for r in res][:sample_size]
            knobs[cnt] = [get_full_knobs_dict(r[1]) for r in res][:sample_size]
            print str(i)+"'s representative knob: " + str(knobs[cnt][0])
            print str(i)+"'s data: " + str(len(data[cnt]))
            cnt += 1
        print "========="

    return data, knobs


if __name__ == '__main__':

    data, knobs = get_data_and_knobs(False, 30000)

    fake_run_id = "123456"
    y_key = 'overhead'
    exp_count = len(knob_names) * len(knob_values[0])
    print "exp_count: " + str(exp_count)

    FactorialAnova(fake_run_id, y_key, knob_names, exp_count).start(data, knobs)