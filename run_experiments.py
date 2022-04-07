from experiment_1 import experiment_1
from experiment_2 import experiment_2
from experiment_3 import experiment_3
from experiment_0 import experiment_0
from experiment_4 import experiment_4
from experiment_5 import experiment_5
from experiment_6 import experiment_6
from experiment_7 import experiment_7
from experiment_8 import experiment_8
from experiment_9 import experiment_9
from experiment_10 import experiment_10
from experiment_11 import experiment_11
from experiment_12 import experiment_12
from experiment_13 import experiment_13
from experiment_14 import experiment_14

import sys

import cProfile

if __name__ == '__main__':
    # cProfile.run('experiment_5.run()', 'stats')
    # import pstats
    # from pstats import SortKey
    # p = pstats.Stats('stats')
    # p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(10)
    args = sys.argv   
    run_type = int(args[1])    
    #run_type = 12
    if run_type == 1:
        experiment_1.run()

    elif run_type == 2:
        experiment_2.run()
    
    elif run_type == 3:
        experiment_3.run()
    
    elif run_type == 4:
        experiment_4.run()
    
    elif run_type == 5:
        experiment_5.run()
    
    elif run_type == 6:
        experiment_6.run()
    
    elif run_type == 7:
        experiment_7.run()
    
    elif run_type == 8:
        experiment_8.run()
    
    elif run_type == 9:
        experiment_9.run()

    elif run_type == 10:
        experiment_10.run()
    
    elif run_type == 11:
        experiment_11.run()

    elif run_type == 12:
        experiment_12.run()
    
    elif run_type == 13:
        experiment_13.run()    
    
    elif run_type == 14:
        experiment_14.run()
