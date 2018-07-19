from sqlalchemy import create_engine, func
from sqlalchemy.sql import select, text
import os
from numpy import around, array, float, mean, std, ndarray
from itertools import combinations
from scipy.stats import ttest_ind, f_oneway

db_file_name = 'arguments.db'
if os.path.isfile(db_file_name):
    engine = create_engine('///'.join(['sqlite:', db_file_name]))
else:
    raise Exception('The following file %s does not exist: ' % db_file_name)

conn = engine.connect()

def getTTest(sql):
    s = text(sql)
    twType_vs_times = {}
    twTypes = []
    result = {}
    for r in conn.execute(s).fetchall():
        tw_type = r['tw_type'] + '_' + r['argument_type']
        twTypes.append(tw_type)
        # it converts an array of strings to an array of floats in numpy.
        times = r['responses'].split(',')
        twType_vs_times[tw_type] = array(times, dtype='|S4').astype(float)
    twTypes_combinations = list(combinations(twTypes, 2))
    for twTypes_combination in twTypes_combinations:
        a = twType_vs_times[twTypes_combination[0]]
        b = twType_vs_times[twTypes_combination[1]]
        label = ' vs '.join([twTypes_combination[0], twTypes_combination[1]])
        mean_a = round(mean(a), 2)
        mean_b = round(mean(b), 2)
        std_a = round(std(a), 2)
        std_b = round(std(b), 2)
        t, p = ttest_ind(a, b, equal_var=True)
        result[label] = around([t , p * 18, mean_a, std_a, mean_b, std_b], decimals=3).tolist()
    return result
