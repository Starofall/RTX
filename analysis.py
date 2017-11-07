from rtxlib.rtx_run import setup_database
from rtxlib.rtx_run import db
from analysis_lib.one_sample_tests import KolmogorovSmirnov
from analysis_lib.two_sample_tests import Ttest
from scipy import stats


if __name__ == "__main__":

    setup_database()
    results = db().get_all_data_points()

    res0 = [res for res in results if res[1]["route_random_sigma"]==0]
    res1 = [res for res in results if res[1]["route_random_sigma"]==0.1]
    res2 = [res for res in results if res[1]["route_random_sigma"]==0.2]
    res4 = [res for res in results if res[1]["route_random_sigma"]==0.4]
    res6 = [res for res in results if res[1]["route_random_sigma"]==0.6]
    res8 = [res for res in results if res[1]["route_random_sigma"]==0.8]

    print "0's: " + str(len(res0))
    print "1's: " + str(len(res1))
    print "2's: " + str(len(res2))
    print "4's: " + str(len(res4))
    print "6's: " + str(len(res6))
    print "8's: " + str(len(res8))

    data0 = dict()
    knobs0 = dict()
    data0[0] = [r[0] for r in res0]
    knobs0[0] = [r[1] for r in res0]
    print "length 0: " + str(len(data0[0]))

    data2 = dict()
    knobs2 = dict()
    data2[0] = [r[0] for r in res2]
    knobs2[0] = [r[1] for r in res2]
    print "length 0.2: " + str(len(data2[0]))

    data = data0
    data0[0] = data0[0][:40000]
    data0[1] = data2[0][:40000]

    y_key = "overhead"
    fake = "vdffd"

    res = Ttest(fake, y_key, alpha=0.05).start(data0, knobs0)
    print "Ttest: " + str(res)

    res = KolmogorovSmirnov(fake, y_key, alpha=0.05).start(data2, knobs2)
    print res
