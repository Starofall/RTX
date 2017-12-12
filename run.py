from rtxlib import info
from rtxlib.rtx_run import RTXRun
import sys
from rtxlib.rtx_run import setup_database


if __name__ == "__main__":

    setup_database()
    target_system_name = sys.argv[1]
    strategy = eval(sys.argv[2])
    info("Running rtx on target system with name: " + target_system_name)
    info(len(strategy["knobs"]))
    RTXRun.create(target_system_name, strategy).run()

    import time
    end = time.time()
    print "simulation finished"
    print end - float(sys.argv[3])
    # print "simulation finished: " + time.strftime('%X %x %Z')