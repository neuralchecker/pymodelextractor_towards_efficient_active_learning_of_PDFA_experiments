from experiment_1 import experiment_1
from experiment_2 import experiment_2
from experiment_3 import experiment_3
from experiment_4 import experiment_4


import sys

if __name__ == '__main__':    
    args = sys.argv   
    run_type = int(args[1]) 
   
    if run_type == 1:
        experiment_1.run()

    elif run_type == 2:
        experiment_2.run()
    
    elif run_type == 3:
        experiment_3.run()
    
    elif run_type == 4:
        experiment_4.run()    