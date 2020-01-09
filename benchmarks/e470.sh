#!/usr/bin/env bash
taskset -c 0 /home/numair/Videos/crab-llvm/py/optAI.py --benchmarkFolder="/home/numair/Videos/crab-llvm/benchmarks/uaf1/" --optAlgo="dars" --timeOut=120 --iterations=40 &
taskset -c 1 /home/numair/Videos/crab-llvm/py/optAI.py --benchmarkFolder="/home/numair/Videos/crab-llvm/benchmarks/uaf2/" --optAlgo="dars" --timeOut=120 --iterations=40 & 
taskset -c 2 /home/numair/Videos/crab-llvm/py/optAI.py --benchmarkFolder="/home/numair/Videos/crab-llvm/benchmarks/uaf3/" --optAlgo="dars" --timeOut=120 --iterations=40 &
taskset -c 3 /home/numair/Videos/crab-llvm/py/optAI.py --benchmarkFolder="/home/numair/Videos/crab-llvm/benchmarks/uaf4/" --optAlgo="dars" --timeOut=120 --iterations=40
