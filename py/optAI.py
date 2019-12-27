#!/usr/bin/env python3
import os
from random import randint
import sets
import math

ALL_DOMAINS = ['int', 'ric', 'term-int',
                'dis-int', 'term-dis-int', 'boxes',  
                'zones', 'oct', 'pk',
                'as-int', 'as-ric', 'as-term-int', 
                'as-dis-int', 'as-term-dis-int', 'as-boxes', 
                'as-zones', 'as-oct', 'as-pk',
                'bool']
CHEAP_DOMAINS = []
USABLE_LIST_OF_DOMAINS = ALL_DOMAINS
WIDENING_DELAYS = [1, 2, 4, 8, 16]
NARROWING_ITERATIONS = [1, 2, 3, 4]
WIDENING_JUMP_SETS = [0, 10, 20, 30, 40]



def argument_parser():
    import argparse
    parser = argparse.ArgumentParser(description='wrapper for optAI')
    parser.add_argument('--inputFile', help="path to input C file")
    parser.add_argument('--optAlgo', help="Optimization Algorithm")
    parser.add_argument('--timeOut', help="Time out")
    args = vars(parser.parse_args())
    return args



def synthesize_optAI_flags(parameters):
    """
        inputs:
            parameters: dict()
        outputs:
            Flags that are only accepted and processed by autoAI
    """

    # Number of domains
    domains = " --domains=" + str(parameters["domains"])
    # domain names
    list_of_domains = " --dom1=" + str(parameters['dom1'])
    list_of_domains = list_of_domains + " --dom2=" + str(parameters["dom2"]) if parameters["domains"] > 1 else list_of_domains
    list_of_domains = list_of_domains + " --dom3=" + str(parameters["dom3"]) if parameters["domains"] > 2 else list_of_domains
    # backward flags for each domain
    list_of_backwardFlags = " --back1" if parameters["back1"] == 1 else ""
    list_of_backwardFlags = list_of_backwardFlags + " --back2" if parameters["back2"] == 1 and parameters["domains"] > 1 else list_of_backwardFlags
    list_of_backwardFlags = list_of_backwardFlags + " --back3" if parameters["back3"] == 1 and parameters["domains"] > 2 else list_of_backwardFlags
    # Global Variables
    global_variables = " --crab-widening-delay=" + str(parameters["wid_delay"])
    global_variables = global_variables + " --crab-narrowing-iterations=" + str(parameters["narr_iter"])
    global_variables = global_variables + " --crab-widening-jump-set=" + str(parameters["wid_jump_set"]) 

    flags = " --autoAI" + domains + list_of_domains + list_of_backwardFlags + global_variables
    return flags


def random_sampling():
    """
        Step1: Randomly choose the number of domains
        Step2: Choose random domains from the list of ALL DOMAINS
        Step3: Choose backward flagfor each domain
        Step4: Choose global variables
    """
    parameters = dict()
    
    print("######### optAI.py: Optimization strategy = Random Sampling")
    number_of_domains = randint(1,3)
    parameters["domains"] = number_of_domains
    print("######### optAI.py: Number of domains selected = " + str(number_of_domains))
    parameters["dom1"] = USABLE_LIST_OF_DOMAINS[randint(0, len(USABLE_LIST_OF_DOMAINS)-1)]
    parameters["dom2"] = USABLE_LIST_OF_DOMAINS[randint(0, len(USABLE_LIST_OF_DOMAINS)-1)] if number_of_domains > 1 else None
    parameters["dom3"] = USABLE_LIST_OF_DOMAINS[randint(0, len(USABLE_LIST_OF_DOMAINS)-1)] if number_of_domains > 2 else None
    parameters["back1"] = randint(0,1)
    parameters["back2"] = randint(0,1)
    parameters["back3"] = randint(0,1)
    parameters["wid_delay"] = WIDENING_DELAYS[randint(0, len(WIDENING_DELAYS)-1)]
    parameters["narr_iter"] = NARROWING_ITERATIONS[randint(0, len(NARROWING_ITERATIONS)-1)]
    parameters["wid_jump_set"] = WIDENING_JUMP_SETS[randint(0, len(WIDENING_JUMP_SETS)-1)]

    print("######### optAI.py: dom1 = " + str(parameters["dom1"]) + " " + str(parameters["back1"]) )
    print("######### optAI.py: dom2 = " + str(parameters["dom2"]) + " " + str(parameters["back2"]) )
    print("######### optAI.py: dom3 = " + str(parameters["dom3"]) + " " + str(parameters["back3"]) )
    print("######### optAI.py: Widening delay = " + str(parameters["wid_delay"]))
    print("######### optAI.py: narrowing iteration = " + str(parameters["narr_iter"]))
    print("######### optAI.py: Widening Jump Set = " + str(parameters["wid_jump_set"]))

    return parameters


def dars():
    def get_addition_candidate_domains(currentConfiguration):
        """
            Given a configuration, return a set of possible next domains,
            that respect the lattice
            ALGORITHM:
                <1> : union of all incomparable elements in the current configuration
                <2> : union of all comparable elements in the current configuration
                <3> : union of <2> and current configuration
                <4> : difference of <1> and <3>
        """
        # <1>
        incomp_union = []
        for element in currentConfiguration:
            incomp_union = sets.set_union(incomp_union, sets.all_incomparable_elements[element])
        # <2>
        comp_union = []
        for element in currentConfiguration:
            comp_union = sets.set_union(comp_union, sets.all_comparable_elements[element])
        # <3>
        union_comparable_and_current_configuraiton = sets.set_union(comp_union, currentConfiguration)
        # <4>
        candidate_domains = sets.set_difference(incomp_union, union_comparable_and_current_configuraiton)
        return candidate_domains

    print("######### optAI.py: Optimization strategy = LATTICE RANDOM")
    parameters = dict()
    number_of_domains = randint(1,3)
    list_of_domains = []
    list_of_domains.append(sets.array_normalizer[USABLE_LIST_OF_DOMAINS[randint(0, len(USABLE_LIST_OF_DOMAINS)-1)]])
    for i in range(1, number_of_domains):
        candidate_domains = get_addition_candidate_domains(list_of_domains)
        if len(candidate_domains) > 0:
            list_of_domains.append(candidate_domains[randint(0, len(candidate_domains) - 1)])

    # Random array flip for the selected list of domains
    parameters["dom1"] = list_of_domains[0] if randint(0,1) == 0 else sets.array_flip[list_of_domains[0]]
    if len(list_of_domains) > 1:
        parameters["dom2"] = list_of_domains[1] if randint(0,1) == 0 else sets.array_flip[list_of_domains[1]]
    else:
        parameters["dom2"] = None
    if len(list_of_domains) > 2:
        parameters["dom3"] = list_of_domains[2] if randint(0,1) == 0 else sets.array_flip[list_of_domains[2]]
    else:
        parameters["dom3"] = None

    print("######### optAI.py: Number of domains selected = " + str(number_of_domains))
    print("######### optAI.py: Number of domains we got = " + str(len(list_of_domains)))
    parameters["domains"] = len(list_of_domains)
    parameters["back1"] = randint(0,1)
    parameters["back2"] = randint(0,1)
    parameters["back3"] = randint(0,1)
    print("######### optAI.py: dom1 = " + str(parameters["dom1"]) + " " + str(parameters["back1"]) )
    print("######### optAI.py: dom2 = " + str(parameters["dom2"]) + " " + str(parameters["back2"]) )
    print("######### optAI.py: dom3 = " + str(parameters["dom3"]) + " " + str(parameters["back3"]) )

    parameters["wid_delay"] = WIDENING_DELAYS[randint(0, len(WIDENING_DELAYS)-1)]
    parameters["narr_iter"] = NARROWING_ITERATIONS[randint(0, len(NARROWING_ITERATIONS)-1)]
    parameters["wid_jump_set"] = WIDENING_JUMP_SETS[randint(0, len(WIDENING_JUMP_SETS)-1)]

    # some sanity checks
    if len(list_of_domains) == 1 :
        assert(parameters["dom1"] is not None)
    if len(list_of_domains) == 2 :
        assert(parameters["dom1"] is not None)
        assert(parameters["dom2"] is not None)
    if len(list_of_domains) == 3 :
        assert(parameters["dom1"] is not None)
        assert(parameters["dom2"] is not None)
        assert(parameters["dom3"] is not None)

    return parameters

def hill_climbing():
    optAI_flags = ""
    print("NOT YET IMPLEMENTED")
    return optAI_flags




def simulated_annealing():
    """
        Simulated annealing optimization algorithm
    """

    optAI_flags = ""
    return optAI_flags




def baysian_optimization():
    """
    TODO: maybe use ROBO ?
    """
    optAI_flags = ""
    print("NOT YET IMPLEMENTED")
    return optAI_flags






##############################
############## Util fFunctions


def initial_configuration():
    inital_configuration = {
        "domains" : 1,
        "dom1" : "bool",
        "dom2" : None,
        "dom2" : None,
        "back1" : 0,
        "back2" : 0,
        "back3" : 0,
        "wid_delay" : 1,
        "narr_iter" : 1,
        "wid_jump_set" : 0
    }
    return inital_configuration


def get_cost(run_command, input_file_path, timeout):
    """
        Run the final command and get the cost of the configuration
    """    
    input_file_path = input_file_path.replace("/", "_")
    input_file_path = input_file_path.replace(".", "_")
    result_file_name = input_file_path + ".txt"
    actual_results_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), result_file_name)
    result_file_path = " --resultPath='" + actual_results_file_path + "'"
    run_command = run_command + result_file_path

    print("######### optAI.py: Sythesized Command: " + run_command)
    os.system(run_command)


    cost = math.inf # cost intialized to inf
    # Read the results
    try:
        with open(actual_results_file_path, 'r') as f:
            lines = f.read().splitlines()
    except Exception as e:
        print("######### optAI.py: Error while opening results file")
        print(e)
        return 0
    
    warnings = None
    time = None
    for line in lines:
        if line.find("Warnings:") != -1:
            warnings = line.replace("Warnings:", "")
        if line.find("RunningTime:") != -1:
            time = line.replace("RunningTime:", "") # This time is in milli seconds

    print("######### optAI.py: WARNINGS = " + warnings)
    print("######### optAI.py: TIME = " + time + " MILLI-SECONDS") # This time is in milli seconds

    # delete the temporary results file
    os.system("rm -rf " + actual_results_file_path)


    # compute cost
    assert(warnings is not None)
    assert(time is not None)
    
    #Convert time out to milli seconds
    timeout = float(timeout) * 1000
    warnings = float(warnings)
    time = float(time)

    if time > timeout:
        cost = math.inf
    else:
        boostingFactor = 1000
        cost = (boostingFactor / warnings) * (warnings + (time/timeout))

        #TODO: GET TOTAL NUMBER OF WARNINGS TO COMPUTE COST









############## Util functions end
#################################

def main():
    """
    python wrapper for optAI
    @author: numair@mpi-sws.org
    """

    # Input arguments to this wrapper
    args = argument_parser()
    

    
    # Get argument variables
    path_to_c_file = args["inputFile"]
    optimizationAlgorithm = args["optAlgo"]
    timeout = args["timeOut"]

    if path_to_c_file is None:
        print("PLEASE ENTER PATH TO INPUT C FILE [--inputFile]")
        return 1
    
    if optimizationAlgorithm is None:
        print("PLEASE SPECIFY AN OPTIMIZATION STRATEGY [--optAlgo]")
        return 1

    if timeout is None:
        print("PLEASE PROVIDE TIMEOUT [--timeOut]")
        return 1


    # Intialize variables   
    run_command = ""
    timeout_kill = "timeout " + timeout + "s "
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("/py", "")
    path_to_clamPy = os.path.join(dir_path, "build", "_DIR_", "bin", "clam.py")
    basic_clam_flags = " --crab-check=assert --crab-do-not-print-invariants"

    # Inital run command    
    run_command = timeout_kill + path_to_clamPy + basic_clam_flags + " " + path_to_c_file






    # get configuration
    if optimizationAlgorithm == "rs":
        configuration = random_sampling()
    if optimizationAlgorithm == "dars":
        configuration = dars()
    if optimizationAlgorithm == "sa":
        configuration= simulated_annealing()
    if optimizationAlgorithm == "hc":
        configuration = hill_climbing()
    if optimizationAlgorithm == "bo":
        configuration = baysian_optimization()




    optAI_flags = synthesize_optAI_flags(configuration)
    run_command = run_command + optAI_flags


    # run_command without result_path
    get_cost(run_command, path_to_c_file, timeout)


if __name__ == '__main__':
    print("######### optAI.py: RANDOM SEED NOT SET")
    main()
