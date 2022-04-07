from pymodelextractor.learners.observation_table_learners.pdfa_lstar_learner import PDFALStarLearner
from pymodelextractor.learners.observation_table_learners.pdfa_lstarcol_learner import PDFALStarColLearner
from pymodelextractor.learners.observation_tree_learners.pdfa_quantization_n_ary_tree_learner import PDFAQuantizationNAryTreeLearner
from pythautomata.model_comparators.wfa_tolerance_comparison_strategy import WFAToleranceComparator
from pythautomata.model_comparators.wfa_quantization_comparison_strategy import WFAQuantizationComparator
from pythautomata.base_types.alphabet import Alphabet
from pythautomata.base_types.symbol import SymbolStr
from pymodelextractor.teachers.pdfa_teacher import PDFATeacher 
from pythautomata.utilities import pdfa_metrics
from pythautomata.utilities.sequence_generator import SequenceGenerator
from pythautomata.utilities import pdfa_generator
from pythautomata.utilities import nicaud_dfa_generator
from utilities.utils import compute_stats

import numpy as np
import pandas as pd
import datetime
from  utilities import utils, constants
import joblib
import os
from tqdm import tqdm

#Experiment variating alphabet size
def generate_and_persist_random_PDFAs():
    path = './instances/exp2/'
    try:
        pdfas = utils.load_pdfas(path)
        if len(pdfas) == 0:
            assert(False)
        print('Instances succesfully loaded!')
    except:
        print('Failed loading instances!')
        print('Generating instances...')
        nominal_size = 100
        alphabet_sizes = [2, 4, 8, 16, 32]
        n=10
        counter = 0
        pdfas = []
        pbar = tqdm(total=n*len(alphabet_sizes))
        for alphabet_size in alphabet_sizes:
            counter = 0
            for i in range(n):
                dfa = nicaud_dfa_generator.generate_dfa(alphabet = constants.get_n_ary_alphabet(alphabet_size), nominal_size= nominal_size, seed = counter)
                dfa.name = "random_PDFA_nominal_size_"+str(nominal_size)+"_alphabet_"+str(alphabet_size)+str(counter)     
                pdfa = pdfa_generator.pdfa_from_dfa(dfa)           
                pdfas.append(pdfa)
                joblib.dump(pdfa, filename = path+dfa.name)
                counter += 1    
                pbar.update(1) 
        pbar.close() 
    return pdfas
    

def experiment_random_PDFAS():
    print(os.listdir())    
    pdfas = generate_and_persist_random_PDFAs()
    tolerance = 0.001
    partitions = int(1/tolerance)
    tolerance_comparator = WFAToleranceComparator(tolerance)
    partition_comparator = WFAQuantizationComparator(partitions)
    algorithms = [('WLStarLearner',PDFALStarLearner, tolerance_comparator, tolerance), ('QuantNaryTreeLearner', PDFAQuantizationNAryTreeLearner, partition_comparator, partitions)]
    
    results = []   
    number_of_executions  = 10
    print('Excecuting extraction...')
    pbar = tqdm(total=number_of_executions*len(algorithms)*len(pdfas))
    for (algorithm_name,algorithm, comparator, param) in algorithms:
        for pdfa in pdfas:
            for i in range(number_of_executions):
                pdfa_teacher = PDFATeacher(pdfa, comparator)
                learner = algorithm()
                secs, result = utils.time_fun(learner.learn,pdfa_teacher, param)               
                pbar.update(1)    
                if i > 0:
                    if algorithm_name == 'QuantNaryTreeLearner':
                        ot_suff = None
                        ot_pref = None
                        if result.info['observation_tree'] is None:
                            tree_depth = 0
                            inner_nodes = 0
                        else:
                            tree_depth = result.info['observation_tree'].depth
                            inner_nodes = result.info['observation_tree'].inner_nodes
                    else:
                        ot_suff = len(result.info['observation_table'].get_suffixes())
                        ot_pref = len(result.info['observation_table'].get_observed_sequences())
                        tree_depth = None
                        inner_nodes = None
                    extracted_model = result.model
                    log_probability_error, wer,ndcg, out_of_partition, out_of_tolerance, absolute_error_avg  = compute_stats(pdfa, extracted_model, tolerance = tolerance, partitions = partitions)
                    results.append((algorithm_name, pdfa.name, len(pdfa.weighted_states), len(extracted_model.weighted_states), i, secs, result.info['last_token_weight_queries_count'], result.info['equivalence_queries_count'], ot_pref, ot_suff, tree_depth, inner_nodes ,log_probability_error, wer,ndcg, out_of_partition, out_of_tolerance, len(pdfa.alphabet)))
    pbar.close() 
    dfresults = pd.DataFrame(results, columns = ['Algorithm', 'Instance', 'Number of States', 'Extracted Number of States','RunNumber','Time (s)','LastTokenQuery', 'EquivalenceQuery', 'OT Prefixes', 'OT Suffixes', 'Tree Depth', 'Inner Nodes','LogProbError','WER','NDCG','OOPartition','OOTolerance', 'Alphabet Size']) 
    dfresults.to_csv('./experiment_2/results/results_'+datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")+'.csv') 

def run():
    experiment_random_PDFAS()
