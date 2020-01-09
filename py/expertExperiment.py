#!/usr/bin/env python3
import csv
import sets
import re
import optAI
import os


def extract_domains(intial_list):
    """
    Returns 2 lists, domains, backward
    """
    domains = list()
    backward = list()

    for domain in intial_list:
        if domain != "":
            backward_flag = re.sub(r'\D', "", domain)
            backward.append(backward_flag)
            remove_string = "<<" + backward_flag + ">>"
            domains.append(domain.replace(remove_string, ""))
    return domains, backward


def import_results(path_to_results):
    """
    results :  {  file_1 :{    domains : [] ,
                                backward: [] ,
                                global : []
                            },

                    file_2  : { domains : [],
                                backward : [], 
                                global : []
                              }
                    .
                    .
                    .
                    .                                
                }
    """

    results = dict()
    with open(path_to_results, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            if row[0] == "File_path":
                continue
            inital_list = row[11:14]
            domains, backward = extract_domains(inital_list)
            results[row[0]] = { 
                    "domains"  : domains ,
                    "backward" : backward,
                    "global"   : row[8:11],
                    "safe"     : row[1],
                    "warnings" : row[2]
            } 
    return results



def run_configuration():
    """
    run optAI.py with --expertExp mode
    and get the result
    """



def main():

    # Step 1
    # Read the csv file and load all the best configurations.
    # Random sampling
    path_to_results = "/home/numair/Videos/crab-llvm/py/sa.csv"
    # checkout import_results to see how results look like            
    results = import_results(path_to_results)

    # Step 2:
    # For a file, run the best configuraiton

    list_of_filePaths = list(results.keys())


    for path_to_input_file in list_of_filePaths:
        #path_to_input_file = "/home/numair/Videos/crab-llvm/benchmarks/e470_3/sipr16k_DivByZeroCheck_IntOverflowManualCheck_BufferOverflowCheck_UseAfterFreeShadowCheck.bc"
        domains = results[path_to_input_file]["domains"]
        print(domains)
        backward = results[path_to_input_file]["backward"]
        print(backward)
        global_settings = results[path_to_input_file]["global"]
        print(global_settings)
        timeout = "2"
        expert = True
        server = None
        new_results = optAI.run_config(path_to_input_file, domains, backward, global_settings, timeout, expert, server)
        print("recieved analysis resutls securely.")

        # Step 3:
        # Compare the results
        # If there are less warnings then that means that the expert domain was able to solve something more
        # We just need that number
        # These are the new assertions solved by the expert domain
        new_assertions = int(results[path_to_input_file]["warnings"]) - int(new_results["warnings"])
        print("Number of new assertions solved by the expert domain = " + str(new_assertions))

        ## Run the original domain on the original file
        original_analysis_results = optAI.run_config(path_to_input_file, ["orig-zones"], ["0"], ["1", "3", "0"], "1.5", False, None)
        

        export_file_path = "/home/numair/Videos/crab-llvm/py/expert.csv"
        if not os.path.exists(export_file_path):
            f = open(export_file_path, "a+")    
            f.write("File_path,new assertions solved by expert, assertions solved by expert on orig file\n")
            f.close()
        f = open(export_file_path, "a+")
        f.write(path_to_input_file + ",")   # file_path
        f.write(str(new_assertions) + ",") # new assertions solved by the expert recipe
        f.write(str(original_analysis_results["safe"]) + ",") # new assertions solved by the expert recipe
        f.write("\n")
        f.close()


if __name__ == '__main__':
    main()

    #file_path = "/home/numair/Videos/crab-llvm/benchmarks/e470_3/t_set_DivByZeroCheck_IntOverflowManualCheck_BufferOverflowCheck_UseAfterFreeShadowCheck.bc"
    #domains = ["orig-zones"]
    #backward = ["0"]
    #global_settings = ["1", "3", "0"]
    #analysis_results = optAI.run_config(file_path, domains, backward, global_settings, "500", False, None)
    #print("GOT " + str(analysis_results["warnings"]) + "warnings for this file")
    #print("GOT " + str(analysis_results["safe"]) + " safe")