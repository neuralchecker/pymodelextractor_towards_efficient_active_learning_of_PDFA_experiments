from experiment_1 import experiment_1
from experiment_2 import experiment_2
from experiment_3 import experiment_3
from experiment_4 import experiment_4
from experiment_5 import experiment_5
from experiment_6 import experiment_6
from experiment_7 import experiment_7


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
        
    elif run_type == 5:
        experiment_5.run()  
        
    elif run_type == 6:
        experiment_6.run() 
        
    elif run_type == 7:
        experiment_7.run() 