import numpy as np
from scipy import stats
import pickle

with open("complaints_data.pickle", "rb") as pickle_in:
    all_complaints = pickle.load(pickle_in)

for idx in [0.0, 0.2, 0.4, 0.6]:
    c_all = np.array(all_complaints[idx])

    cmpl_num = np.sum(c_all)
    all_num = np.size(c_all)

    success_probability = 0.2
    p_val = stats.binom_test(cmpl_num, all_num, success_probability, alternative="greater")
    p_val2 = stats.binom_test(cmpl_num * 2, all_num * 2, success_probability, alternative="greater")

    print('Idx ' + str(idx) +  '-- ratio: '+ str(cmpl_num) + ' / ' + str(all_num) + ' = ' + str(cmpl_num/float(all_num)) + \
          ', p-value for p > ' + str(success_probability) + ': ' + str(p_val) + ', p-value for 2x more: ' + str(p_val2))
