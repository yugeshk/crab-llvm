#!/usr/bin/env python3

import csv
import re
import optAI
import sets
import math


ALL_DOMAINS = ['int', 'ric', 'term-int',
                'dis-int', 'term-dis-int', 'boxes',  
                'zones', 'oct', 'pk',
                'as-int', 'as-ric', 'as-term-int', 
                'as-dis-int', 'as-term-dis-int', 'as-boxes', 
                'as-zones', 'as-oct', 'as-pk',
                'bool']

WIDENING_DELAYS = [1, 2, 4, 8, 16]
NARROWING_ITERATIONS = [1, 2, 3, 4]
WIDENING_JUMP_SETS = [0, 10, 20, 30, 40]

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
                    "warnings" : row[2],
                    "time" 	   : row[3]
            } 
    return results





def main():
	print("Toggle Experiment")
	
	'''
		EQUAL : The mutated recipe proves the same number of assertions within +- 5 seconds of the orig.
		POSITIVE: The mutated recipe proves more assertions or the equal number of assertions 5 seconds faster
		NEGATIVE: The mutated recipe either proves fewer assertions or the same number of assetions atleast 5
					seconds slower
	'''


	# Widening Delay toggle

	# Try all widening delay except for the original one

	# Narrowing Iteration toggle

	# Widening Threshold toggle

	# Array Smashing toggle

	# Backward analysis toggle

	# Abstract domain toggle

	# Ingredient ordering


	path_to_results = "/home/numair/Videos/crab-llvm/py/dars.csv"
	export_file_path = "/home/numair/Videos/crab-llvm/py/toggle.csv"
	results = import_results(path_to_results)
	list_of_filePaths = list(results.keys())

	f = open(export_file_path, "a+")
	f.write("file_path " + ",")
	f.write("wd_equal " + ",")
	f.write("wd_better " + ",")
	f.write("wd_worse " + ",")
	f.write("ni_equal " + ",")
	f.write("ni_better " + ",")
	f.write("ni_worse " + ",")
	f.write("wt_equal " + ",")
	f.write("wt_better " + ",")
	f.write("wt_worse " + ",")
	f.write("as_equal" + ",")
	f.write("as_better" + ",")
	f.write("as_worse" + ",")
	f.write("backward_equal" + ",")
	f.write("backward_better" + ",")
	f.write("backward_worse" + ",")
	f.write("domain_equal" + ",")
	f.write("domain_better" + ",")
	f.write("domain_worse" + ",")
	f.write("order_equal" + ",")
	f.write("order_better" + ",")
	f.write("order_worse" + ",")
	f.close()

	for path_to_input_file in list_of_filePaths:
		orig_domains = results[path_to_input_file]["domains"]
		orig_backward = results[path_to_input_file]["backward"]
		orig_global_settings = results[path_to_input_file]["global"]
		orig_safe = float(results[path_to_input_file]["safe"])
		orig_time = float(results[path_to_input_file]["time"])
		orig_widening_delay = orig_global_settings[0]
		orig_narrowing_iterations = orig_global_settings[1]
		orig_widening_jump_set = orig_global_settings[2] 


		wd_worse = 0
		wd_better = 0
		wd_equal = 0

		ni_worse = 0
		ni_better = 0
		ni_equal = 0

		wt_worse = 0
		wt_better = 0
		wt_equal = 0

		array_worse = 0
		array_better = 0
		array_equal = 0

		backward_worse = 0
		backward_better = 0
		backward_equal = 0

		domain_worse = 0
		domain_better = 0
		domain_equal = 0

		order_worse = 0
		order_better = 0
		order_equal = 0




		print("--")

		# Toggle the file
		for wd in WIDENING_DELAYS:
			if str(wd) != orig_widening_delay:
				# run this configuration 
				# and send the result to the safe checker
				print("Running with widening delay = " + str(wd))
				
				run = optAI.run_config(path_to_input_file, 
						orig_domains, 
						orig_backward, 
						[wd, orig_narrowing_iterations, orig_widening_jump_set],
						"300",
						expert=False,
						server=None)
				
				if run["time"] == math.inf:
					wd_worse += 1
				else:
					if run["safe"] > orig_safe:
						wd_better += 1
					if run["safe"] < orig_safe:
						wd_worse += 1
					if run["safe"] == orig_safe:
						if run["time"] <= orig_time + 5000 and run["time"] >= orig_time - 5000:
							wd_equal += 1
						if run["time"] < orig_time - 5000:
							wd_better += 1
						if run["time"] > orig_time + 5000:
							wd_worse += 1

		f = open(export_file_path, "a+")
		f.write("\n")
		f.write(path_to_input_file + ",")
		f.write(str(wd_equal) + ",")
		f.write(str(wd_better) + ",")
		f.write(str(wd_worse) + ",")
		f.close()

###############################################################################################
###############################################################################################

		for ni in NARROWING_ITERATIONS:
			if str(ni) != orig_narrowing_iterations:
				print("running with Narrowing iteration = " + str(ni))

				run = optAI.run_config(path_to_input_file, 
						orig_domains, 
						orig_backward, 
						[orig_widening_delay, ni, orig_widening_jump_set],
						"300",
						expert=False,
						server=None)

				if run["time"] == math.inf:
					ni_worse += 1
				else:
					if run["safe"] > orig_safe:
						ni_better += 1
					if run["safe"] < orig_safe:
						ni_worse += 1
					if run["safe"] == orig_safe:
						if run["time"] <= orig_time + 5000 and run["time"] >= orig_time - 5000:
							ni_equal += 1
						if run["time"] < orig_time - 5000:
							ni_better += 1
						if run["time"] > orig_time + 5000:
							ni_worse += 1

		f = open(export_file_path, "a+")
		f.write(str(ni_equal) + ",")
		f.write(str(ni_better) + ",")
		f.write(str(ni_worse) + ",")
		f.close()



###############################################################################################
###############################################################################################

		for wt in WIDENING_JUMP_SETS:
			if str(wt) != orig_widening_jump_set:
				print("running with Widening Jump set = " + str(wt))


				run = optAI.run_config(path_to_input_file, 
						orig_domains, 
						orig_backward, 
						[orig_widening_delay, orig_narrowing_iterations, wt],
						"300",
						expert=False,
						server=None)


				if run["time"] == math.inf:
					wt_worse += 1
				else:
					if run["safe"] > orig_safe:
						wt_better += 1
					if run["safe"] < orig_safe:
						wt_worse += 1
					if run["safe"] == orig_safe:
						if run["time"] <= orig_time + 5000 and run["time"] >= orig_time - 5000:
							wt_equal += 1
						if run["time"] < orig_time - 5000:
							wt_better += 1
						if run["time"] > orig_time + 5000:
							wt_worse += 1


		f = open(export_file_path, "a+")
		f.write(str(wt_equal) + ",")
		f.write(str(wt_better) + ",")
		f.write(str(wt_worse) + ",")
		f.close()


###############################################################################################
###############################################################################################
# Array Smashing

		# For all the domains, flip the array smashing of that domain
		for i in range(0, len(orig_domains)):
			domains = orig_domains
			flipped_domain = sets.array_flip[orig_domains[i]]
			domains[i] = flipped_domain

			run = optAI.run_config(path_to_input_file, 
						domains, 
						orig_backward, 
						orig_global_settings,
						"300",
						expert=False,
						server=None)

			if run["time"] == math.inf:
				array_worse += 1
			else:
				if run["safe"] > orig_safe:
					array_better += 1
				if run["safe"] < orig_safe:
					array_worse += 1
				if run["safe"] == orig_safe:
					if run["time"] <= orig_time + 5000 and run["time"] >= orig_time - 5000:
						array_equal += 1
					if run["time"] < orig_time - 5000:
						array_better += 1
					if run["time"] > orig_time + 5000:
						array_worse += 1


		f = open(export_file_path, "a+")
		f.write(str(array_equal) + ",")
		f.write(str(array_better) + ",")
		f.write(str(array_worse) + ",")
		f.close()


###############################################################################################
###############################################################################################
# Backward

		# For all the domains, flip the backward
		for i in range(0, len(orig_domains)):
			backward = orig_backward
			backward[i] = str(abs(int(backward[i]) - 1))

			run = optAI.run_config(path_to_input_file, 
						orig_domains, 
						backward, 
						orig_global_settings,
						"300",
						expert=False,
						server=None)

			if run["time"] == math.inf:
				backward_worse += 1
			else:
				if run["safe"] > orig_safe:
					backward_better += 1
				if run["safe"] < orig_safe:
					backward_worse += 1
				if run["safe"] == orig_safe:
					if run["time"] <= orig_time + 5000 and run["time"] >= orig_time - 5000:
						backward_equal += 1
					if run["time"] < orig_time - 5000:
						backward_better += 1
					if run["time"] > orig_time + 5000:
						backward_worse += 1


		f = open(export_file_path, "a+")
		f.write(str(backward_equal) + ",")
		f.write(str(backward_better) + ",")
		f.write(str(backward_worse) + ",")
		f.close()


###############################################################################################
###############################################################################################
# Change a domain to a comparable domain
		
		for i in range(0, len(orig_domains)):

			# Is it an array smashing domain ?
			as_domain = sets.array_smashing_domain(orig_domains[i])

			# First normalize the domain
			domain = sets.array_normalizer[orig_domains[i]]

			# Generate all comparable elements of this domain
			comparable_domains = sets.all_comparable_elements[domain]

			for comp_domain in comparable_domains:
				domains_to_run = orig_domains
				if as_domain:
					domains_to_run[i] = sets.array_flip[comp_domain]
				else:
					domains_to_run[i] = comp_domain

				run = optAI.run_config(path_to_input_file, 
						domains_to_run, 
						backward, 
						orig_global_settings,
						"300",
						expert=False,
						server=None)


				if run["time"] == math.inf:
					domain_worse += 1
				else:
					if run["safe"] > orig_safe:
						domain_better += 1
					if run["safe"] < orig_safe:
						domain_worse += 1
					if run["safe"] == orig_safe:
						if run["time"] <= orig_time + 5000 and run["time"] >= orig_time - 5000:
							domain_equal += 1
						if run["time"] < orig_time - 5000:
							domain_better += 1
						if run["time"] > orig_time + 5000:
							domain_worse += 1

		f = open(export_file_path, "a+")
		f.write(str(domain_equal) + ",")
		f.write(str(domain_better) + ",")
		f.write(str(domain_worse) + ",")
		f.close()



###############################################################################################
###############################################################################################
# Change the order of the domains


		if len(orig_domains) == 1:
			pass
		elif len(orig_domains) == 2:
			domain_1 = orig_domains[0]
			domain_2 = orig_domains[1]
			run = optAI.run_config(path_to_input_file, 
						[domain_2, domain_1], 
						backward, 
						orig_global_settings,
						"300",
						expert=False,
						server=None)

			if run["time"] == math.inf:
					order_worse += 1
			else:
				if run["safe"] > orig_safe:
					order_better += 1
				if run["safe"] < orig_safe:
					order_worse += 1
				if run["safe"] == orig_safe:
					if run["time"] <= orig_time + 5000 and run["time"] >= orig_time - 5000:
						order_equal += 1
					if run["time"] < orig_time - 5000:
						order_better += 1
					if run["time"] > orig_time + 5000:
						order_worse += 1
		else:
			# length of the config is 3
			dom1 = orig_domains[0]
			dom2 = orig_domains[1]
			dom3 = orig_domains[2]

			list_of_configs = [ [dom1, dom3, dom2], 
								[dom2, dom1, dom3],
								[dom2, dom3, dom1],
								[dom3, dom1, dom2],
								[dom3, dom2, dom1]
							]
			for domain_order in list_of_configs:

				run = optAI.run_config(path_to_input_file, 
						domain_order, 
						backward, 
						orig_global_settings,
						"300",
						expert=False,
						server=None)

				if run["time"] == math.inf:
					order_worse += 1
				else:
					if run["safe"] > orig_safe:
						order_better += 1
					if run["safe"] < orig_safe:
						order_worse += 1
					if run["safe"] == orig_safe:
						if run["time"] <= orig_time + 5000 and run["time"] >= orig_time - 5000:
							order_equal += 1
						if run["time"] < orig_time - 5000:
							order_better += 1
						if run["time"] > orig_time + 5000:
							order_worse += 1
		

		f = open(export_file_path, "a+")
		f.write(str(order_equal) + ",")
		f.write(str(order_better) + ",")
		f.write(str(order_worse) + ",")
		f.close()




if __name__ == '__main__':
    main()


# Hello my name is numair mansur, 
# what is your name ?

