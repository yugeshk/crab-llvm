#!/usr/bin/env python3

import os
import optAI



def argument_parser():
    import argparse
    parser = argparse.ArgumentParser(description='wrapper for optAI')
    parser.add_argument('--benchmarkFolder', help="Path to benchmark folder")
    args = vars(parser.parse_args())
    return args


def export_data(export_file_path, file, best_safe, best_warnings, best_time):
    if not os.path.exists(export_file_path):
        f = open(export_file_path, "a+")
        f.write("File_path,safe,warnings,time(ms)\n")
        f.close()
    f = open(export_file_path, "a+")
    f.write(file + ",")   # file_path
    f.write(str(best_safe) + ",") # best safe
    f.write(str(best_warnings) + ",") # best warnings 
    f.write(str(best_time) + ",") # best time
    f.write("\n")
    f.close()






def main():
    """
        ./bestrecipe.py --benchmarkFolder="/home/numair/Videos/crab-llvm/benchmarks/best1/"
    """

    args = argument_parser()
    path_to_benchmark_folder = args["benchmarkFolder"]
    export_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "best.csv")

    list_of_files = []

    for r, d, f in os.walk(path_to_benchmark_folder):
        for file in f:
            list_of_files.append(os.path.join(r, file))
    
    print("loaded " + str(len(list_of_files)) + " files in memory")
    
    # Intialize variables   
    timeout = "1800"
    timeout_kill = "timeout " + timeout + "s "
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("/py", "")
    path_to_clamPy = os.path.join(dir_path, "build", "_DIR_", "bin", "clam.py")
    basic_clam_flags = " --crab-check=assert --crab-do-not-print-invariants --crab-disable-warnings --crab-track=arr --crab-singleton-aliases"
    basic_clam_flags = basic_clam_flags + " --crab-heap-analysis=cs-sea-dsa --crab-do-not-store-invariants --devirt-functions=types --externalize-addr-taken-functions"
    basic_clam_flags = basic_clam_flags + " --lower-select --lower-unsigned-icmp" 
        

    for file_path in list_of_files:
        # Run command to run the most precise domain on a file
        run_command = timeout_kill + path_to_clamPy + basic_clam_flags + " " + file_path + " --autoAI --mostPrecise"
        print("RUN COMMAND")
        print(run_command)
        
        config_cost = optAI.get_cost(run_command, file_path, timeout, "best")  

        warnings = 0
        time = 0
        total_assertions = 0
        safe = 0

        if config_cost[0] == "timeout":
            warnings = "timeout"
            time = "timeout"
            total_assertions = "timeout"
            safe = "timeout"
        else:
            warnings = float(config_cost[1])
            time = float(config_cost[2])
            total_assertions = float(config_cost[3])
            safe = total_assertions - warnings

        export_data(export_file_path, file_path, safe, warnings, time)

if __name__ == '__main__':
    main()
    #path_to_input_file = "/home/numair/Videos/crab-llvm/benchmarks/benchmarks2/11.bc"
    #original_analysis_results = optAI.run_config(path_to_input_file, ["as-zones"], ["1"], ["16", "4", "40"], "50", False, None)