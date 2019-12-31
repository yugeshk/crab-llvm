#!/usr/bin/env bash
taskset -c 1 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks1/" --optAlgo="dars" --timeOut=1 --iterations=40 --server=1 &
taskset -c 2 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks2/" --optAlgo="dars" --timeOut=1 --iterations=40 --server=1 &
taskset -c 3 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks3/" --optAlgo="dars" --timeOut=1 --iterations=40 --server=1 &
taskset -c 4 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks4/" --optAlgo="dars" --timeOut=1 --iterations=40 --server=1 &
taskset -c 5 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks5/" --optAlgo="dars" --timeOut=1 --iterations=40 --server=1 &
taskset -c 6 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks6/" --optAlgo="dars" --timeOut=1 --iterations=40 --server=1 &
taskset -c 7 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks1/" --optAlgo="rs" --timeOut=1 --iterations=40 --server=1 &
taskset -c 8 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks2/" --optAlgo="rs" --timeOut=1 --iterations=40 --server=1 &
taskset -c 9 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks3/" --optAlgo="rs" --timeOut=1 --iterations=40 --server=1 &
taskset -c 10 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks4/" --optAlgo="rs" --timeOut=1 --iterations=40 --server=1 &
taskset -c 11 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks5/" --optAlgo="rs" --timeOut=1 --iterations=40 --server=1 &
taskset -c 12 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks6/" --optAlgo="rs" --timeOut=1 --iterations=40 --server=1 &
taskset -c 13 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks1/" --optAlgo="sa" --timeOut=1 --iterations=40 --server=1 &
taskset -c 14 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks2/" --optAlgo="sa" --timeOut=1 --iterations=40 --server=1 &
taskset -c 15 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks3/" --optAlgo="sa" --timeOut=1 --iterations=40 --server=1 &
taskset -c 16 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks4/" --optAlgo="sa" --timeOut=1 --iterations=40 --server=1 &
taskset -c 17 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks5/" --optAlgo="sa" --timeOut=1 --iterations=40 --server=1 &
taskset -c 18 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks6/" --optAlgo="sa" --timeOut=1 --iterations=40 --server=1 &
taskset -c 19 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks1/" --optAlgo="hc" --timeOut=1 --iterations=40 --server=1 &
taskset -c 20 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks2/" --optAlgo="hc" --timeOut=1 --iterations=40 --server=1 &
taskset -c 21 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks3/" --optAlgo="hc" --timeOut=1 --iterations=40 --server=1 &
taskset -c 22 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks4/" --optAlgo="hc" --timeOut=1 --iterations=40 --server=1 &
taskset -c 23 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks5/" --optAlgo="hc" --timeOut=1 --iterations=40 --server=1 &
taskset -c 24 /home/bmariano/crab-llvm/py/optAI.py --benchmarkFolder="/home/bmariano/crab-llvm/benchmarks/benchmarks6/" --optAlgo="hc" --timeOut=1 --iterations=40 --server=1
# 3 experiments
# --timeOut=1 --iterations=40
# --timeOut=300 --iterations=40
# --timeOut=300 --iterations=40
