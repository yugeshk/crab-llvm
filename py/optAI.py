#!/usr/bin/env python3
import os

def argument_parser():
    import argparse
    parser = argparse.ArgumentParser(description='wrapper for optAI')
    parser.add_argument('--inputFile', help="path to input C file")
    args = vars(parser.parse_args())
    return args


def random_sampling():
    pass

def dars():
    pass

def hill_climbing():
    pass

def simulated_annealing():
    pass

def baysian_optimization():
    pass




def synthesize_optAI_flags():
 
    result_path = "--resultPath=" + os.path.join(os.path.dirname(os.path.realpath(__file__)), "result.txt")
    

    # TODO: Determine the size of the configuration (min 1, max 3)
    # --domains= n
    # Determine the domains
    # --dom1=. --dom2= ......
    # Determine the backward
    # --back1, --back2, --back3
    # Determine the global variables


    flags = " --autoAI " + result_path
    return flags










def main():
    """
    python wrapper for optAI
    @author: numair@mpi-sws.org
    """

    # Input arguments to this wrapper
    args = argument_parser()
    

    

    # Get argument variables
    path_to_c_file = args["inputFile"]


    if path_to_c_file is None:
        print("PLEASE ENTER PATH TO INPUT C FILE")
        return 1


    # Intialize variables   
    run_command = ""
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("/py", "")
    path_to_clamPy = os.path.join(dir_path, "build", "_DIR_", "bin", "clam.py")
    basic_clam_flags = " --crab-check=assert --crab-do-not-print-invariants"

    # Inital run command    
    run_command = path_to_clamPy + basic_clam_flags + " " + path_to_c_file

    # get optAI flags
    optAI_flags = synthesize_optAI_flags()

    run_command = run_command + optAI_flags









    #file_path = "/home/numair/Videos/crab-llvm/build/_DIR_/bin/test.c"
    #dir_path = os.path.dirname(os.path.realpath(__file__)).replace("/py", "")
    #path_to_clamPy = os.path.join(dir_path, "build", "_DIR_", "bin", "clam.py")
    #run_command = path_to_clamPy + " --crab-do-not-print-invariants --crab-check=assert " + file_path + " --autoAI --domains=3 --dom1=bool --dom2=bool --dom3=bool --resultPath='/home/numair/Videos/results.txt'"
    os.system(run_command)


if __name__ == '__main__':
    main()