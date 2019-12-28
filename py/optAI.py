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
    print("######### optAI.py: Optimization strategy = LATTICE RANDOM")
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

    print("######### optAI.py: Widening delay = " + str(parameters["wid_delay"]))
    print("######### optAI.py: narrowing iteration = " + str(parameters["narr_iter"]))
    print("######### optAI.py: Widening Jump Set = " + str(parameters["wid_jump_set"]))

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




def mutation_algorithm(previous_configuration, onlyModifyDomains):
    """
        Simulated annealing optimization algorithm
    """
    # First get the list of domains. This i the only thing we care about in a config
    print("######### optAI.py: Optimization strategy = SIMULATED ANNEALING")
    successful_mutation  = False
    new_configuration = []
    # Extract only domains
    if onlyModifyDomains:
        # Array normalize the domains
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
        if action == 1 and len(new_configuration) < 3 :
            # ADDTION
            # add the LEAST IN-COMPARABLE DOMAIN
            print("######### optAI.py: addition action chosen")
            candidate_domains = sets.get_addition_candidate_domains_for_mutation_algo(new_configuration)
            if len(candidate_domains) > 0:
                new_configuration.append(candidate_domains[randint(0, len(candidate_domains) - 1)])
                successful_mutation = True
        else:
            # Modificaiton
            print("######### optAI.py: modification action chosen")
            # First decide a modification location
            mod_loc = randint(0, len(new_configuration) - 1)
            print("######### optAI.py: mod location = " + str(mod_loc))
            # Decide a sub-action: 
            # 1: higher in the lattice  50%
            # 2: lower in the lattice   30%
            # 3: some least incomparable    20%
            sub_action_pool = [1,1,1,1,1,2,2,2,3,3]
            sub_action = sub_action_pool[randint(0, len(sub_action_pool)-1)]
            candidate_domains = []
            if sub_action == 1:
                print("######### optAI.py: sub-action = [1] one step higher comparable in the lattice")
                candidate_domains = sets.one_step_higher_comparable_elements[new_configuration[mod_loc]]
                # Take difference from the current configuraiton
                candidate_domains = sets.set_difference(candidate_domains, new_configuration)
            if sub_action == 2: 
                print("######### optAI.py: sub-action = [2] one step lower comparable in the lattice")
                candidate_domains = sets.one_step_lower_comparable_elements[new_configuration[mod_loc]]
                # Take difference from the current configuraiton
                candidate_domains = sets.set_difference(candidate_domains, new_configuration)
                # Check that the candidate_domains set does not contain an element that is lower_comaprable to any
                # element in new_configuration   
                lower_comparable_union = sets.get_lower_comparable_domains(new_configuration)
                candidate_domains = sets.set_difference(candidate_domains, lower_comparable_union)
            if sub_action == 3:
                print("######### optAI.py: sub-action = [3] least íncomparable")
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

    print("######### optAI.py: dom1 = " + str(parameters["dom1"]) + " " + str(parameters["back1"]) )
    print("######### optAI.py: dom2 = " + str(parameters["dom2"]) + " " + str(parameters["back2"]) )
    print("######### optAI.py: dom3 = " + str(parameters["dom3"]) + " " + str(parameters["back3"]) )

    print("######### optAI.py: Widening delay = " + str(parameters["wid_delay"]))
    print("######### optAI.py: narrowing iteration = " + str(parameters["narr_iter"]))
    print("######### optAI.py: Widening Jump Set = " + str(parameters["wid_jump_set"]))

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


def hill_climbing():
    optAI_flags = ""
    print("NOT YET IMPLEMENTED")
    return optAI_flags



def baysian_optimization():
    """
    TODO: maybe use ROBO.py ?
    """
    print("NOT YET IMPLEMENTED")
    return {"domains" : 0}






##############################
############## Util Functions


def initial_configuration():
    inital_configuration = {
        "domains" : 1,
        "dom1" : "pk",
        "dom2" : None,
        "dom3" : None,
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
    total_assertions = None
    for line in lines:
        if line.find("Warnings:") != -1:
            warnings = line.replace("Warnings:", "")
        if line.find("RunningTime:") != -1:
            time = line.replace("RunningTime:", "") # This time is in milli seconds
        if line.find("TotalAssertions:") != -1:
            total_assertions = line.replace("TotalAssertions:", "")

   
    assert(warnings is not None)
    assert(time is not None)
    assert(total_assertions is not None)

    print("######### optAI.py: WARNINGS = " + warnings)
    print("######### optAI.py: TIME = " + time + " MILLI-SECONDS") # This time is in milli seconds
    print("######### optAI.py: TOTAL ASSERTIONS = " + total_assertions)

    # delete the temporary results file
    os.system("rm -rf " + actual_results_file_path)


    # Compute cost
    
    #Convert time out to milli seconds
    timeout = float(timeout) * 1000
    warnings = float(warnings)
    time = float(time)
    total_assertions = float(total_assertions)

    if total_assertions == 0:
        print("######### optAI.py: TOTAL ASSERTIONS = 0. NO ASSERTIONS FOUND IN THIS PROGRAM")
        return 0

    if time > timeout:
        cost = math.inf
    else:
        boostingFactor = 1000
        cost = (boostingFactor / total_assertions) * (warnings + (time/timeout))

    print("######### optAI.py: COST of the configuration = " + str(cost))
    return cost



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
    timeout_kill = "timeout " + timeout + "s "
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("/py", "")
    path_to_clamPy = os.path.join(dir_path, "build", "_DIR_", "bin", "clam.py")
    basic_clam_flags = " --crab-check=assert --crab-do-not-print-invariants"

    # Inital run command    
    prefix_run_command = timeout_kill + path_to_clamPy + basic_clam_flags + " " + path_to_c_file




    # Initializations before the optimization loop
    initial_optAI_flag = synthesize_optAI_flags(initial_configuration())
    initial_run_command = prefix_run_command + initial_optAI_flag
    initial_cost = get_cost(initial_run_command, path_to_c_file, timeout)
    previous_config_cost = initial_cost
    previous_configuration = initial_configuration()
    new_configuration = previous_configuration
    best_cost = initial_cost
    best_config = initial_configuration()


    # Start optimization loop
    for loop_step in range(50,0,-1):
        # get configuration
        print("***********************************")
        print("***********************************")
        print("***********************************")
        print("***********************************")
        print("***********************************")
        print("****** OPTIMIZATION LOOP " + str(loop_step) + " ********")
        print("***********************************")
        print("***********************************")
        print("***********************************")
        print("***********************************")
        print("***********************************")
        if optimizationAlgorithm == "rs":
            configuration = random_sampling()

        if optimizationAlgorithm == "dars":
            configuration = dars()

        if optimizationAlgorithm == "sa":
            onlyModifyDomains = True if loop_step >= 5 else False
            new_configuration= mutation_algorithm(previous_configuration, onlyModifyDomains)
        
        if optimizationAlgorithm == "hc":
            configuration = hill_climbing()

        if optimizationAlgorithm == "bo":
            configuration = baysian_optimization()
       

        optAI_flags = synthesize_optAI_flags(new_configuration)
        run_command = prefix_run_command + optAI_flags

        #run_command without result_path
        new_configuration_cost =  get_cost(run_command, path_to_c_file, timeout)       
        acceptanceProb = acceptance_probability(previous_config_cost, new_configuration_cost, loop_step)
        # Decide whether to accept the configuraiton or not
        if accept_configuration(optimizationAlgorithm, acceptanceProb):
            previous_configuration = new_configuration
            previous_config_cost = new_configuration_cost
            # Best configuration
            if new_configuration_cost < best_cost:
                best_cost = new_configuration_cost
                best_config = new_configuration
    
    
    print("######### optAI.py: BEST CONFIGURATION ")
    print(best_config["dom1"] + " " + str(best_config["back1"]))
    print(str(best_config["dom2"]) + " " + str(best_config["back2"]))
    print(str(best_config["dom3"]) + " " + str(best_config["back3"]))
    print("best cost = " + str(best_cost))
    print("intial cost = " + str(initial_cost))





if __name__ == '__main__':
    print("######### optAI.py: RANDOM SEED NOT SET")
    main()
