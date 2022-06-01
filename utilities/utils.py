
import timeit
import joblib
import os, sys
from pythautomata.utilities import pdfa_metrics
from pythautomata.utilities.sequence_generator import SequenceGenerator

def compute_stats(target_model, extracted_model, tolerance, partitions, test_sequences = None, sample_size = 1000, max_seq_length = 20, seed = 42):
    if test_sequences is None:
        sg = SequenceGenerator(target_model.alphabet, max_seq_length, seed)
        test_sequences = sg.generate_words(sample_size)
    
    log_probability_error = pdfa_metrics.log_probability_error(target_model, extracted_model, test_sequences)
    wer = pdfa_metrics.wer_avg(target_model, extracted_model, test_sequences)
    ndcg = pdfa_metrics.ndcg_score_avg(target_model, extracted_model, test_sequences)
    out_of_partition = pdfa_metrics.out_of_partition_elements(
        target_model, extracted_model, test_sequences, partitions)
    out_of_tolerance = pdfa_metrics.out_of_tolerance_elements(
        target_model, extracted_model, test_sequences, tolerance)
    absolute_error_avg = pdfa_metrics.absolute_error_avg(target_model, extracted_model, test_sequences)
    return log_probability_error, wer,ndcg, out_of_partition, out_of_tolerance, absolute_error_avg


def time_fun(function, *args):    
    t0 = timeit.default_timer()
    result = function(*args)
    t1 = timeit.default_timer()
    total_seconds = t1-t0
    return total_seconds, result

def load_pdfas(path):
    dirs = os.listdir( path )
    if len(dirs) == 0:
        raise Exception('No file found')
    pdfas = []
    for file in dirs:
        print(file)
        if file != '.ipynb_checkpoints':
            pdfa = joblib.load(path+file)
            pdfas.append(pdfa)
    return pdfas

def load_dfas(path):
    dirs = os.listdir( path )
    if len(dirs) == 0:
        raise Exception('No file found')
    dfas = []
    for file in dirs:
        print(file)
        dfa = joblib.load(path+file)
        dfas.append(dfa)
    return dfas