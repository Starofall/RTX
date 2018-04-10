from rtxlib import info, error
from rtxlib.execution import experimentFunction
from colorama import Fore
import requests, json

header = {"content-type": "application/json"}
connection_err_msg = {"error": "Connection with R server is failed"}
host_with_port = ""


def start_mlr_mbo_strategy(wf):
    global host_with_port
    host_with_port = "http://" + str(wf.host) + ":" + str(wf.port)
    """ executes mlr MBO strategy """
    info("> ExecStrategy   | mlr MBO", Fore.CYAN)
    optimizer_iterations = wf.execution_strategy["optimizer_iterations"]
    optimizer_iterations_in_design = wf.execution_strategy["optimizer_iterations_in_design"]
    wf.totalExperiments = optimizer_iterations + optimizer_iterations_in_design # also include number of samples in design to it
    acquisition_method = wf.execution_strategy["acquisition_method"]

    # we look at the ranges the user has specified in the knobs
    knobs = wf.execution_strategy["knobs"]
    info("> Initial knobs   | " + str(knobs), Fore.CYAN)

    if optimizer_iterations_in_design < len(knobs) * 4:
        error("Initial design is not large enough, please update definition.py")
        return

    # we create a list of variable names and a list of knob (min, max)
    json_array = []
    for key in knobs:
        knob_object = dict()
        knob_object["name"] = key
        knob_object["min"] = knobs[key][0]
        knob_object["max"] = knobs[key][1]
        json_array.append(knob_object)

    request_body = dict(
        id=wf.rtx_run_id,
        wf=dict(
            acquisition_method=acquisition_method,
            optimizer_iterations=optimizer_iterations,
            optimizer_iterations_in_design=optimizer_iterations_in_design,
            knobs=json_array
        )
    )
    result = initiate_mlr_mbo(wf, request_body)
    if result is not None:
        info("> ExecStrategy mlrMBO  | " + str(result), Fore.CYAN)
    else:
        error("> ExecStrategy mlrMBO  | error occurred, see the logs")
    return

def initiate_mlr_mbo(wf, request_body):
    try:
        api = host_with_port + "/mlrMBO/initiate"
        r = requests.post(api, data=json.dumps(request_body), headers=header)
        res = r.json()
        if res[0] and res[1]:
            initial_design_knobs = res[1]
            initial_design_values = []
            for knob in initial_design_knobs:
                exp = create_experiment_tuple(wf, knob)
                value = float(experimentFunction(wf, exp))
                # value = random.uniform(1, 4) # TODO: will be replaced by actual implementation
                initial_design_values.append(value)
            # now update the design with calculated outputs
            return update_initial_design(wf, initial_design_values)
        else:
            err_msg = {"error": "Cannot fetch initial design proposal/values, make sure R server is up and running"}
            error(err_msg)
            return None
    except requests.ConnectionError as e:
        error(connection_err_msg)
        return None


''' updates mlrMBO design by sending outputs in a HTTP POST request '''
def update_initial_design(wf, initial_design_values):
    try:
        body = dict(
            id=wf.rtx_run_id,
            initial_design_values=initial_design_values
        )
        api = host_with_port + "/mlrMBO/initialDesign/update"
        r = requests.post(api, data=json.dumps(body), headers=header)
        res = r.json()
        if "result" in res:
            if res["result"] is True:
                # if it reaches this point, then initial state is done, we should create artifacts
                return create_artifacts(wf)
            else:
                err_msg = {"error": res["result"]}
                error(err_msg)
                return None
        else:
            err_msg = {"error": "Cannot update initial design values, make sure R server is up and running"}
            error(err_msg)
            return None
    except requests.ConnectionError as e:
        error(connection_err_msg)
        return None

''' triggers R side to create acquisition criteria & MBO controll and calls initSMBO function '''
def create_artifacts(wf):
    try:
        body = dict(
            id=wf.rtx_run_id
        )
        api = host_with_port + "/mlrMBO/createArtifacts"
        r = requests.post(api, data=json.dumps(body), headers=header)
        res = r.json()
        if "result" in res:
            if res["result"] is True:
                # if it reaches this point, then mlrMBO is started to propose points,
                # so we run experimentFunction, calculate values, and re-update the smbo state
                # assumption: we only get one point tuple from smbo for each iteration
                info("> ExecStrategy   | mlrMBO artifacts created successfully", Fore.CYAN)
                iteration_index = 0
                successful_update = True
                while iteration_index < wf.execution_strategy["optimizer_iterations"]:
                    if successful_update is True:
                        proposed_points = get_proposed_points(wf)
                        if proposed_points:
                            info("> Proposed points  | " + str(proposed_points))
                            # value = random.uniform(1, 4) # TODO: will be replaced by actual implementation
                            exp = create_experiment_tuple(wf, proposed_points)
                            value = float(experimentFunction(wf, exp))
                            successful_update = update_mbo_state(wf, proposed_points, value)
                        else:
                            err_msg = {"error": "Error occurred while running experimentFunction and getting new proposed points"}
                            error(err_msg)
                            return None
                    iteration_index += 1
                return finalize_optimization(wf)
            else:
                err_msg = {"error": res["result"]}
                error(err_msg)
                return None
        else:
            err_msg = {"error": "Cannot create artifacts, make sure R server is up and running"}
            error(err_msg)
            return None
    except requests.ConnectionError as e:
        error(connection_err_msg)
        return None

def update_mbo_state(wf, proposed_points, value):
    try:
        body = dict(
            id=wf.rtx_run_id,
            knobs=proposed_points,
            value=value
        )
        api = host_with_port + "/mlrMBO/model/update"
        r = requests.post(api, data=json.dumps(body), headers=header)
        res = r.json()
        if "result" in res:
            return True
        else:
            err_msg = {"error": "An error occurred in updating mlrMBO model, please restart the optimization"}
            error(err_msg)
            return False

    except requests.ConnectionError as e:
        error(connection_err_msg)
        return None

def get_proposed_points(wf):
    try:
        body = dict(
            id=wf.rtx_run_id
        )
        api = host_with_port + "/mlrMBO/model/getProposedPoint"
        r = requests.post(api, data=json.dumps(body), headers=header)
        res = r.json()
        if res:
            return res[0]
        elif "result" in res:
            err_msg = {"error": res["result"]}
            error(err_msg)
            return None
        else:
            err_msg = {"error": "Unexpected error occurred while getting proposed points"}
            error(err_msg)
            return None
    except requests.ConnectionError as e:
        error(connection_err_msg)
        return None


def create_experiment_tuple(wf, knobs):
    exp = dict()
    exp["ignore_first_n_results"] = wf.execution_strategy["ignore_first_n_results"]
    exp["sample_size"] = wf.execution_strategy["sample_size"]
    exp["knobs"] = knobs
    return exp


def finalize_optimization(wf):
    try:
        body = dict(
            id=wf.rtx_run_id
        )
        api = host_with_port + "/mlrMBO/finalize"
        r = requests.post(api, data=json.dumps(body), headers=header)
        res = r.json()
        if "result" in res:
            if res["result"] is True:
                return "MLR strategy has ended"
            else:
                err_msg = {"error": res["result"]}
                error(err_msg)
                return None
        else:
            err_msg = {"error": "An error occurred in finalizing mlrMBO optimization"}
            error(err_msg)
            return None
    except requests.ConnectionError as e:
        error(connection_err_msg)
        return None