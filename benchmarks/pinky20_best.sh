#!/usr/bin/env bash
taskset -c 1 /home/bmariano/crab-llvm/py/bestrecipe.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks1/" &
taskset -c 2 /home/bmariano/crab-llvm/py/bestrecipe.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks2/" &
taskset -c 3 /home/bmariano/crab-llvm/py/bestrecipe.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks3/" & 
taskset -c 4 /home/bmariano/crab-llvm/py/bestrecipe.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks4/" &
taskset -c 5 /home/bmariano/crab-llvm/py/bestrecipe.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks5/" &
taskset -c 6 /home/bmariano/crab-llvm/py/bestrecipe.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks6/"
