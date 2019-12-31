#!/usr/bin/env bash
taskset -c 0 /home/numair/Videos/crab-llvm/py/optAI.py --benchmarkFolder="/home/numair/Videos/crab-llvm/benchmarks/e470_1/" --optAlgo="rs" --timeOut=1 --iterations=40 &
taskset -c 1 /home/numair/Videos/crab-llvm/py/optAI.py --benchmarkFolder="/home/numair/Videos/crab-llvm/benchmarks/e470_2/" --optAlgo="rs" --timeOut=1 --iterations=40 & 
taskset -c 2 /home/numair/Videos/crab-llvm/py/optAI.py --benchmarkFolder="/home/numair/Videos/crab-llvm/benchmarks/e470_3/" --optAlgo="rs" --timeOut=1 --iterations=40 &
taskset -c 3 /home/numair/Videos/crab-llvm/py/optAI.py --benchmarkFolder="/home/numair/Videos/crab-llvm/benchmarks/e470_4/" --optAlgo="rs" --timeOut=1 --iterations=40
