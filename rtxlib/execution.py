from colorama import Fore

from rtxlib import info, error, warn, direct_print, process, log_results


def experimentFunction(wf, exp):
    # remove all old data from the queues
    wf.data_provider.reset()

    # start
    info(">")
    info("> KnobValues     | " + str(exp["knobs"]))

    # create new state
    exp["state"] = wf.system["state_initializer"](dict())

    # apply changes to system
    try:
        wf.change_provider.applyChange(wf.system["change_event_creator"](exp["knobs"]))
    except:
        error("apply changes did not work")

    # ignore the first data sets
    to_ignore = exp["ignore_first_n_results"]
    if to_ignore > 0:
        i = 0
        while i < to_ignore:
            new_data = wf.data_provider.returnData()
            if new_data is not None:
                i += 1
                process("IgnoreSamples  | ", i, to_ignore)
        print("")

    # start collecting data
    sample_size = exp["sample_size"]
    i = 0
    while i < sample_size:
        new_data = wf.data_provider.returnData()
        if new_data is not None:
            try:
                exp["state"] = wf.system["data_reducer"](exp["state"], new_data)
            except:
                error("could not reducing data set: " + str(new_data))
            i += 1
            process("CollectSamples | ", i, sample_size)
    print("")

    try:
        result = wf.system["evaluator"](exp["state"])
    except:
        result = 0
        error("evaluator failed")

    info("> ResultValue    | " + str(result))
    log_results(wf.folder, exp["knobs"].values() + [result])

    return result