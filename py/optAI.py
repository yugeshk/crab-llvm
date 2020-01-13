#!/usr/bin/env python3
import os
import random
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

USABLE_LIST_OF_DOMAINS = ALL_DOMAINS
WIDENING_DELAYS = [1, 2, 4, 8, 16]
NARROWING_ITERATIONS = [1, 2, 3, 4]
WIDENING_JUMP_SETS = [0, 10, 20, 30, 40]

# Optimization Algorithms

def random_sampling():
    """
        Random Sampling
    """
    parameters = dict()
    print("################## optAI.py: Optimization strategy = Random Sampling")
    number_of_domains = randint(1,3)
    parameters["domains"] = number_of_domains
    parameters["dom1"] = USABLE_LIST_OF_DOMAINS[randint(0, len(USABLE_LIST_OF_DOMAINS)-1)]
    parameters["dom2"] = USABLE_LIST_OF_DOMAINS[randint(0, len(USABLE_LIST_OF_DOMAINS)-1)] if number_of_domains > 1 else None
    parameters["dom3"] = USABLE_LIST_OF_DOMAINS[randint(0, len(USABLE_LIST_OF_DOMAINS)-1)] if number_of_domains > 2 else None
    parameters["back1"] = randint(0,1)
    parameters["back2"] = randint(0,1)
    parameters["back3"] = randint(0,1)
    parameters["wid_delay"] = WIDENING_DELAYS[randint(0, len(WIDENING_DELAYS)-1)]
    parameters["narr_iter"] = NARROWING_ITERATIONS[randint(0, len(NARROWING_ITERATIONS)-1)]
    parameters["wid_jump_set"] = WIDENING_JUMP_SETS[randint(0, len(WIDENING_JUMP_SETS)-1)]
    return parameters


def dars():
    """
        Domain aware random sampling
    """
    print("################## optAI.py: Optimization strategy = LATTICE RANDOM")
    parameters = dict()
    number_of_domains = randint(1,3)
    list_of_domains = []
    list_of_domains.append(sets.array_normalizer[USABLE_LIST_OF_DOMAINS[randint(0, len(USABLE_LIST_OF_DOMAINS)-1)]])
    for i in range(1, number_of_domains):
        candidate_domains = sets.get_addition_candidate_domains(list_of_domains)
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

    parameters["domains"] = len(list_of_domains)
    parameters["back1"] = randint(0,1)
    parameters["back2"] = randint(0,1)
    parameters["back3"] = randint(0,1)
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




def mutation_algorithm(previous_configuration, onlyModifyDomains, loop_step, total_optimization_iteration):
    """
        Simulated annealing optimization algorithm
    """
    print("################## optAI.py: Optimization strategy = SIMULATED ANNEALING")
    successful_mutation  = False
    new_configuration = []
    if onlyModifyDomains:
        if previous_configuration["dom1"] != None:
            new_configuration.append(sets.array_normalizer[previous_configuration["dom1"]])
        if previous_configuration["dom2"] != None:
            new_configuration.append(sets.array_normalizer[previous_configuration["dom2"]])    
        if previous_configuration["dom3"] != None:
            new_configuration.append(sets.array_normalizer[previous_configuration["dom3"]])
    else:
        if previous_configuration["dom1"] != None:
            new_configuration.append(previous_configuration["dom1"])
        if previous_configuration["dom2"] != None:
            new_configuration.append(previous_configuration["dom2"])    
        if previous_configuration["dom3"] != None:
            new_configuration.append(previous_configuration["dom3"])


    while(not successful_mutation and onlyModifyDomains):
        # Decide an action: 20% addition, 80% modification
        action_pool = [1,2,2,2] # 1:add, 2:modification
        action = action_pool[randint(0, len(action_pool) - 1)]

        # Line 15,16,17 in Algo 1 in the paper
        maxLength = 1
        if total_optimization_iteration == 80:
            if loop_step < 70:
                maxLength = 2
            if loop_step < 50:
                maxLength = 3
        
        if total_optimization_iteration == 40:
            if loop_step < 35:
                maxLength = 2
            if loop_step < 25:
                maxLength = 3
        #maxLength = 3
        if action == 1 and len(new_configuration) < maxLength :
            # ADDTION
            # add the LEAST IN-COMPARABLE DOMAIN
            candidate_domains = sets.get_addition_candidate_domains_for_mutation_algo(new_configuration)
            if len(candidate_domains) > 0:
                new_configuration.append(candidate_domains[randint(0, len(candidate_domains) - 1)])
                successful_mutation = True
        else:
            # Modificaiton
            # First decide a modification location
            mod_loc = randint(0, len(new_configuration) - 1)
            # Decide a sub-action: 
            # 1: higher in the lattice  50%
            # 2: lower in the lattice   30%
            # 3: some least incomparable    20%
            sub_action_pool = [1,1,1,1,1,2,2,2,3,3]
            sub_action = sub_action_pool[randint(0, len(sub_action_pool)-1)]
            candidate_domains = []
            if sub_action == 1:
                print("################## optAI.py: sub-action = [1] one step higher comparable in the lattice")
                candidate_domains = sets.one_step_higher_comparable_elements[new_configuration[mod_loc]]
                # Take difference from the current configuraiton
                candidate_domains = sets.set_difference(candidate_domains, new_configuration)
            if sub_action == 2: 
                print("################## optAI.py: sub-action = [2] one step lower comparable in the lattice")
                candidate_domains = sets.one_step_lower_comparable_elements[new_configuration[mod_loc]]
                # Take difference from the current configuraiton
                candidate_domains = sets.set_difference(candidate_domains, new_configuration)
                # Check that the candidate_domains set does not contain an element that is lower_comaprable to any
                # element in new_configuration   
                lower_comparable_union = sets.get_lower_comparable_domains(new_configuration)
                candidate_domains = sets.set_difference(candidate_domains, lower_comparable_union)
            if sub_action == 3:
                print("################## optAI.py: sub-action = [3] least íncomparable")
                candidate_domains = sets.get_addition_candidate_domains_for_mutation_algo(new_configuration)
            if len(candidate_domains) > 0 :
                new_configuration[mod_loc] = candidate_domains[randint(0, len(candidate_domains) - 1)]
                successful_mutation = True

    parameters = dict()
    parameters["domains"] = len(new_configuration)
    parameters["back1"] = previous_configuration["back1"]
    parameters["back2"] = previous_configuration["back2"]
    parameters["back3"] = previous_configuration["back3"]
    parameters["wid_delay"] = previous_configuration["wid_delay"]
    parameters["narr_iter"] = previous_configuration["narr_iter"]
    parameters["wid_jump_set"] = previous_configuration["wid_jump_set"]

    # Mutate global + local parameters
    if(not onlyModifyDomains):
        # Random Array Flipping
        for i in range(0, len(new_configuration) - 1) :
            new_configuration[i] = new_configuration[i] if randint(0,1) == 0 else sets.array_flip[new_configuration[i]]
        parameters["back1"] = randint(0,1)
        parameters["back2"] = randint(0,1)
        parameters["back3"] = randint(0,1)
        parameters["wid_delay"] = WIDENING_DELAYS[randint(0, len(WIDENING_DELAYS)-1)]
        parameters["narr_iter"] = NARROWING_ITERATIONS[randint(0, len(NARROWING_ITERATIONS)-1)]
        parameters["wid_jump_set"] = WIDENING_JUMP_SETS[randint(0, len(WIDENING_JUMP_SETS)-1)]

    parameters["dom1"] = new_configuration[0]
    if len(new_configuration) > 1:
        parameters["dom2"] = new_configuration[1]
    else:
        parameters["dom2"] = None
    if len(new_configuration) > 2:
        parameters["dom3"] = new_configuration[2]
    else:
        parameters["dom3"] = None
    # some sanity checks
    if len(new_configuration) == 1 :
        assert(parameters["dom1"] is not None)
    if len(new_configuration) == 2 :
        assert(parameters["dom1"] is not None)
        assert(parameters["dom2"] is not None)
    if len(new_configuration) == 3 :
        assert(parameters["dom1"] is not None)
        assert(parameters["dom2"] is not None)
        assert(parameters["dom3"] is not None)

    return parameters


def hill_climbing(previous_configuration, loop_step, total_optimization_iteration):
    next_configuration = dict()
    if loop_step % 10 == 0:
        next_configuration = dars()
    else:
        onlyModifyDomains = True if loop_step >= 10 else False
        next_configuration = mutation_algorithm(previous_configuration, onlyModifyDomains, loop_step, total_optimization_iteration)
    return next_configuration


def baysian_optimization():
    """
    TODO: maybe use ROBO.py ?
    """
    print("NOT YET IMPLEMENTED")
    return {"domains" : 0}






##############################
############## Util Functions

def argument_parser():
    import argparse
    parser = argparse.ArgumentParser(description='wrapper for optAI')
    parser.add_argument('--inputFile', help="path to input C file")
    parser.add_argument('--optAlgo', help="Optimization Algorithm")
    parser.add_argument('--timeOut', help="Time out")
    parser.add_argument('--benchmarkFolder', help="Path to benchmark folder")
    parser.add_argument('--iterations', help="number of optimization iterations")
    parser.add_argument('--debug', help="debug mode")
    parser.add_argument('--server', help="server")
    parser.add_argument('--seed', help="random seed")
    args = vars(parser.parse_args())
    return args



def synthesize_optAI_flags(parameters, server):
    """
        inputs:
            parameters: dict()
        outputs:
            Flags that are only accepted and processed by autoAI
    """

    # ELINA PK BACKWARD ERROR
    if parameters["dom1"] == "pk" or parameters["dom1"] == "as-pk":
        parameters["back1"] = 0
    if parameters["dom2"] == "pk" or parameters["dom2"] == "as-pk":
        parameters["back2"] = 0
    if parameters["dom3"] == "pk" or parameters["dom3"] == "as-pk":
        parameters["back3"] = 0
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


def initial_configuration():
    inital_configuration = {
        "domains" : 1,
        "dom1" : "bool",
        "dom2" : None,
        "dom3" : None,
        "back1" : 1,
        "back2" : 0,
        "back3" : 0,
        "wid_delay" : 1,
        "narr_iter" : 1,
        "wid_jump_set" : 0
    }
    return inital_configuration


def get_cost(run_command, input_file_path, timeout, algo):
    """
        Run the final command and get the cost of the configuration
    """    
    input_file_path = input_file_path.replace("/", "_")
    input_file_path = input_file_path.replace(".", "_")
    result_file_name = input_file_path + "_" + algo + ".txt"
    actual_results_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), result_file_name)
    result_file_path = " --resultPath='" + actual_results_file_path + "'"
    run_command = run_command + result_file_path

    print("################## optAI.py: Sythesized Command: " + run_command)
    os.system(run_command)


    cost = math.inf # cost intialized to inf
    # Read the results
    try:
        with open(actual_results_file_path, 'r') as f:
            lines = f.read().splitlines()
    except Exception as e:
        print("################## optAI.py: Error while opening results file")
        print(e)
        return "timeout","timeout", "timeout", "timeout"
    
    warnings = None
    time = None
    total_assertions = None
    for line in lines:
        if line.find("Warnings:") != -1:
            warnings = line.replace("Warnings:", "")
        if line.find("RunningTime:") != -1:
            time = line.replace("RunningTime:", "") # This time is in milli seconds
        if line.find("TotalAssertions:") != -1:
            total_assertions = line.replace("TotalAssertions:", "")


    # DO NOT COMPUTE COST IF THE FILE TIMED OUT !
    if warnings == "TIMEOUT":
        print("THE CONFIGURATION TIMED OUT")
        os.system("rm " + actual_results_file_path)        
        return "timeout","timeout", "timeout", "timeout"

    print("################## optAI.py: WARNINGS = " + warnings)
    print("################## optAI.py: SAFE = " + str(int(total_assertions) - int(warnings)))
    print("################## optAI.py: TOTAL ASSERTIONS = " + total_assertions)
    print("################## optAI.py: TIME = " + time + " MILLI-SECONDS") # This time is in milli seconds
    
    # delete the temporary results file
    os.system("rm " + actual_results_file_path)


    # Compute cost
    
    #Convert time out to milli seconds
    timeout = float(timeout) * 1000
    warnings = float(warnings)
    time = float(time)
    total_assertions = float(total_assertions)

    if total_assertions == 0:
        print("################## optAI.py: TOTAL ASSERTIONS = 0. NO ASSERTIONS FOUND IN THIS PROGRAM")
        os.system("rm " + actual_results_file_path)
        return 0,0,0,0

    if time > timeout:
        cost = math.inf
    else:
        boostingFactor = 1000
        cost = (boostingFactor / total_assertions) * (warnings + (time/timeout))

    print("################## optAI.py: COST of the configuration = " + str(cost))
    return cost, warnings, time, total_assertions



def acceptance_probability(previousConfigCost, newConfigurationCost, NumberOfSteps):
    """
        e = previous config
        e' = new config
        T = NumberOfSteps

        *  Implementation of P(e, e', T).
        *  The probability of making a transition from the current state s
        *  to a candidate state s' is specified by the acceptance probability P().
        *  e  ==> getCost(s)
        *  e' ==> getCost(s')
        *  T  ==> Temperature      [number of steps/iterations in our setting].
        * 
        * s and s' are configurations in our setting.
        * 
        * According to the kirkpatrick 1983 paper:
        *   P(e, e', T) =  1                            if e' < e
        *                  exp( -(e' - e) / T )      otherwise
        */
    """
    if newConfigurationCost < previousConfigCost:
        return 1
    else:
        acceptance_prob = pow(2.7, -(newConfigurationCost - previousConfigCost) / NumberOfSteps)
        return acceptance_prob
    


def accept_configuration(optimizationAlgorithm, acceptanceProb):
    if optimizationAlgorithm == "sa":
        random_bw_0_1 = random.random()
        if acceptanceProb  >= random_bw_0_1:
            return True
        else:
            return False
    else:
        # everything else
        return True


def export_data(export_file_path, file, total_assertions, best_safe, best_warnings, best_time, best_cost, best_config, best_iteration, total_iteration_time, time_to_best_iteration):

    print("################## optAI.py: EXPORTING RESULT: " + export_file_path)
    if not os.path.exists(export_file_path):
        f = open(export_file_path, "a+")
        f.write("File_path,safe,warnings,time(ms),cost,best_iteration,total_iteration_time,time_to_best_iteration, wd,nar iter, wd j set, dom1, dom2, dom3\n")
        f.close()
    f = open(export_file_path, "a+")
    f.write(file + ",")   # file_path
    f.write(str(best_safe) + ",") # best safe
    f.write(str(best_warnings) + ",") # best warnings 
    f.write(str(best_time) + ",") # best time
    f.write(str(best_cost) + ",") # best cost
    f.write(str(best_iteration) + ",")  # Number of steps required to reach the best iteration
    f.write(str(total_iteration_time) + ",")    # Total time required to run all iterations
    f.write(str(time_to_best_iteration) + ",")  # Time to best iteration
    f.write(str(best_config["wid_delay"]) + ",") # best wd
    f.write(str(best_config["narr_iter"]) + ",") # best narr iter
    f.write(str(best_config["wid_jump_set"]) + ",") # best wd j set
    f.write(str(best_config["dom1"]) + "<<" +str(best_config["back1"]) + ">>,") # domain  1
    if best_config["dom2"] is not None:
        f.write(str(best_config["dom2"]) + "<<" +str(best_config["back2"]) + ">>,") # domain  2
    if best_config["dom3"] is not None:
        f.write(str(best_config["dom3"]) + "<<" +str(best_config["back3"]) + ">>,") # domain  3
    f.write("\n")
    f.close()


#######################################
#######################################
#### optAI APIs
#######################################
#######################################


def optimize(path_to_input_file, seed=42):
    """
        Find the best recipe for the given program using DARS
    """
    print("Optimizing with DARS")
    configuration = dars()





def run_config(path_to_input_file, domains, backward, global_settings, timeout, expert=False, server=None):
    """
        Runs the config
    """
    
    print("Entered run_config")

    analysis_results = dict()

    # Intialize variables   
    timeout_kill = "timeout " + timeout + "s "
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("/py", "")
    path_to_clamPy = os.path.join(dir_path, "build", "_DIR_", "bin", "clam.py")

    basic_clam_flags = " --crab-check=assert --crab-do-not-print-invariants --crab-disable-warnings --crab-track=arr --crab-singleton-aliases"
    basic_clam_flags = basic_clam_flags + " --crab-heap-analysis=cs-sea-dsa --crab-do-not-store-invariants --devirt-functions=types --externalize-addr-taken-functions"
    basic_clam_flags = basic_clam_flags + " --lower-select --lower-unsigned-icmp" 
        
    # Inital run command    
    prefix_run_command = timeout_kill + path_to_clamPy + basic_clam_flags + " " + path_to_input_file

    # Parameters    
    parameters = dict()
    number_of_domains = len(domains)
    parameters["domains"] = number_of_domains
    parameters["dom1"] = domains[0]
    parameters["dom2"] = domains[1] if number_of_domains > 1 else None
    parameters["dom3"] = domains[2] if number_of_domains > 2 else None
    parameters["back1"] = int(backward[0])
    parameters["back2"] = int(backward[1]) if len(backward) > 1 else 0
    parameters["back3"] = int(backward[2]) if number_of_domains > 2 else 0
    parameters["wid_delay"] = global_settings[0]
    parameters["narr_iter"] = global_settings[1]
    parameters["wid_jump_set"] = global_settings[2]

    # Initializations before the optimization loop
    optAIflags = synthesize_optAI_flags(parameters, server)
    if expert:
        optAIflags = optAIflags + " --expert"

    run_command = prefix_run_command + optAIflags
    config_cost = get_cost(run_command, path_to_input_file, timeout, "expert")
    

    if config_cost[0] == "timeout":
        #print("WHY IS IT TIMING OUT ?")
        #raise KeyboardInterrupt
        warnings = 0
        time = math.inf
        total_assertions = 0
    else:
        cost = float(config_cost[0])
        warnings = float(config_cost[1])
        time = float(config_cost[2])
        total_assertions = float(config_cost[3])


    analysis_results["warnings"] = warnings
    analysis_results["time"] = time
    analysis_results["safe"] = total_assertions - warnings
    
    return analysis_results


#######################################
#######################################
#### optAI APIs end
#######################################
#######################################






#######################################
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
    path_to_benchmark_folder = args["benchmarkFolder"]
    optimization_iterations = args["iterations"]
    server = args["server"]
    seed = args["seed"]

    if path_to_c_file is None and path_to_benchmark_folder is None:
        print("PLEASE ENTER PATH TO INPUT C FILE [--inputFile]")
        return 1
    
    if optimizationAlgorithm is None:
        print("PLEASE SPECIFY AN OPTIMIZATION STRATEGY [--optAlgo]")
        return 1

    if timeout is None:
        print("PLEASE PROVIDE TIMEOUT [--timeOut]")
        return 1

    if optimization_iterations is None:
        print("PLEASE NUMBER OF ITERATIONS FOR OPTIMIZATION [--iterations]")
        return 1

    if seed is None:
        seed = 42
    else:
        seed = int(seed)


    random.seed(seed)

    list_of_files = []
    if path_to_benchmark_folder is not None:
        # extract all the files in this folder. 
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path_to_benchmark_folder):
            for file in f:
                list_of_files.append(os.path.join(r, file))
        print("loaded " + str(len(list_of_files)) + " files in memory")
        for i in list_of_files:
            print(i)

    if path_to_benchmark_folder is None and path_to_c_file is not None:
        list_of_files.append(path_to_c_file)
    
    export_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), optimizationAlgorithm + ".csv")

    file_counter = 0
    for file in list_of_files:
        file_counter += 1
        # Intialize variables   
        timeout_kill = "timeout " + timeout + "s "
        inital_timeout_kill = "timeout 300s "
        dir_path = os.path.dirname(os.path.realpath(__file__)).replace("/py", "")
        path_to_clamPy = os.path.join(dir_path, "build", "_DIR_", "bin", "clam.py")
        basic_clam_flags = " --crab-check=assert --crab-do-not-print-invariants --crab-disable-warnings --crab-track=arr --crab-singleton-aliases"
        basic_clam_flags = basic_clam_flags + " --crab-heap-analysis=cs-sea-dsa --crab-do-not-store-invariants --devirt-functions=types --externalize-addr-taken-functions"
        basic_clam_flags = basic_clam_flags + " --lower-select --lower-unsigned-icmp" 
        
        # Inital run command    
        prefix_run_command = timeout_kill + path_to_clamPy + basic_clam_flags + " " + file
        intial_prefix_run_command = inital_timeout_kill + path_to_clamPy + basic_clam_flags + " " + file

        # Initializations before the optimization loop
        initial_optAI_flag = synthesize_optAI_flags(initial_configuration(), server)
        initial_run_command = intial_prefix_run_command + initial_optAI_flag
        initial_cost = get_cost(initial_run_command, file, timeout, optimizationAlgorithm)
        # This can return timeout here 
        best_warnings = 0
        best_time = 0
        total_assertions = 0
        best_safe = 0
        if initial_cost[0] == "timeout":
            previous_config_cost = math.inf
        else:
            previous_config_cost = float(initial_cost[0])
            best_warnings = float(initial_cost[1])
            best_time = float(initial_cost[2])

        previous_configuration = initial_configuration()
        new_configuration = previous_configuration
        best_cost = previous_config_cost
        best_config = initial_configuration()
        

        if initial_cost[3] == 0:
            print("NO ASSERTION FOUND IN THIS PROGRAM")
            export_data(export_file_path, file, 0, 0, 0, 0, 0, initial_configuration(), 0, 0, 0)
            continue

        best_iteration = 0  # Number of iterations required to reach the best configuration
        total_iteration_time = 0    # Total time required to run all optimization iterations
        best_iteration_time = 0     # Time at best iteration
        time_to_best_iteration = 0  # Time required to reach the best iteration

        # Start optimization loop
        import time
        start_time = time.time()
        for loop_step in range(int(optimization_iterations),1,-1):
            # get configuration
            print("***********************************")
            print("***********************************")
            print("***********************************")
            print("***********************************")
            print("***********************************")
            print("****** Program: " + str(file_counter) + " ****************")
            print("****** OPTIMIZATION LOOP " + str(loop_step) + " ********")
            print("***********************************")
            print("***********************************")
            print("***********************************")
            print("***********************************")
            print("***********************************")
            if optimizationAlgorithm == "rs":
                new_configuration = random_sampling()

            if optimizationAlgorithm == "dars":
                new_configuration = dars()

            if optimizationAlgorithm == "sa":
                # Last 10 iterations only modify settings
                onlyModifyDomains = True if loop_step >= 10 else False
                new_configuration= mutation_algorithm(previous_configuration, onlyModifyDomains, loop_step, int(optimization_iterations))
            
            if optimizationAlgorithm == "hc":
                new_configuration = hill_climbing(previous_configuration, loop_step, int(optimization_iterations))

            if optimizationAlgorithm == "bo":
                new_configuration = baysian_optimization()
        

            optAI_flags = synthesize_optAI_flags(new_configuration, server)
            run_command = prefix_run_command + optAI_flags

            #run_command without result_path
            run_results = get_cost(run_command, file, timeout, optimizationAlgorithm)
            if run_results[0] == "timeout":
                print("timeout!")
                continue
            new_configuration_cost = float(run_results[0])
            warnings = run_results[1]
            config_time = run_results[2]
            total_assertions = run_results[3]
            safe = total_assertions - warnings
            


            acceptanceProb = acceptance_probability(previous_config_cost, new_configuration_cost, loop_step)
            # Decide whether to accept the configuraiton or not
            if accept_configuration(optimizationAlgorithm, acceptanceProb):
                previous_configuration = new_configuration
                previous_config_cost = new_configuration_cost
                # Best configuration
                if new_configuration_cost < best_cost:
                    best_cost = new_configuration_cost
                    best_config = new_configuration
                    best_warnings = warnings
                    best_time = config_time
                    best_safe = safe
                    best_iteration = loop_step
                    best_iteration_time = time.time()

        end_time = time.time()
        total_iteration_time = end_time - start_time
        if best_iteration_time != 0:
            time_to_best_iteration = best_iteration_time - start_time


        
        print("################## optAI.py: BEST CONFIGURATION ")
        print(best_config["dom1"] + " " + str(best_config["back1"]))
        print(str(best_config["dom2"]) + " " + str(best_config["back2"]))
        print(str(best_config["dom3"]) + " " + str(best_config["back3"]))
        print("best cost = " + str(best_cost))
        print("intial cost = " + str(initial_cost))
        print("best_warnings = " + str(best_warnings))
        print("best_safe = " + str(best_safe))
        print("all_iterations_time = " + str(total_iteration_time))

        # Export results
        export_data(export_file_path, file, total_assertions, best_safe, best_warnings, best_time, best_cost, best_config, best_iteration, total_iteration_time, time_to_best_iteration)


if __name__ == '__main__':
    main()




"""
How to use:
./Videos/crab-llvm/py/optAI.py --benchmarkFolder="/home/numair/Videos/benchmarks1/" --optAlgo="sa" --timeOut=1 --iterations=40



[FOR LATER]
* add more domains, especially the cross product of boolean and a numerical domain (The original domains in crab-llvm)

"""