#!/usr/bin/env bash
taskset -c 0 /home/numair/Videos/crab-llvm/py/bestrecipe.py --benchmarkFolder="/home/numair/Videos/crab-llvm/benchmarks/e470_1/" &
taskset -c 1 /home/numair/Videos/crab-llvm/py/bestrecipe.py --benchmarkFolder="/home/numair/Videos/crab-llvm/benchmarks/e470_2/" & 
taskset -c 2 /home/numair/Videos/crab-llvm/py/bestrecipe.py --benchmarkFolder="/home/numair/Videos/crab-llvm/benchmarks/e470_3/" &
taskset -c 3 /home/numair/Videos/crab-llvm/py/bestrecipe.py --benchmarkFolder="/home/numair/Videos/crab-llvm/benchmarks/e470_4/"
