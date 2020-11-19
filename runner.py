#! /usr/bin/python3

import argparse
import json
import matplotlib.pyplot as plt
import numpy as np

from pandas import DataFrame, read_csv
from subprocess import call

BIN_PATH = "kv-bench"
OUT_FILE = "data.json"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backends", type=str, default="all")
    parser.add_argument("--filename", type=str, default="results.csv")
    parser.add_argument("--append", action="store_true", default=False)
    parser.add_argument("--num_iterations", type=int, default=3)
    parser.add_argument("--workloads", type=str, default="all")

    args = parser.parse_args()

    if args.backends == "all":
        backends = ["leveldb", "rocksdb", "lsm"]
    else:
        backends = args.backends.split(',')

    if args.workloads == "all":
        workloads = ["write_only", "read_only"]
    else:
        workloads = args.workloads.split(',')

    for workload in workloads:
        print("Running workload '%s'" % workload)
        run(backends, args.filename, args.append, args.num_iterations, workload)

def run(backends, filename, append, num_iterations, workload):
    key_range = 100*1000
    batch_size = 1000
    total_ops = 500 * 1000

    columns = ["backend", "batch_size", "throughput", "workload"]

    if append:
        results = read_csv(filename)
    else:
        results = DataFrame([], columns=columns)

    num_runs = len(backends) * num_iterations
    count = 0

    for backend in backends:
        for _ in range(num_iterations):
            num_ops = int(total_ops / batch_size)

            call([BIN_PATH, "--backend="+backend, "--workload="+workload, "--batch_size=%i"%batch_size,
                "--sync=true", "--outfile="+OUT_FILE, "--num_ops=%i"%num_ops, "--key_range=%i"%key_range])

            with open(OUT_FILE) as jfile:
                data = json.load(jfile)

            print(str(data))

            result = [backend, batch_size, data["throughput"], workload]
            row = DataFrame([result], columns=columns)
            results = results.append(row)

            results.to_csv(filename, index=False)

            count += 1
            print("Progress: %i out of %i" % (count, num_runs))

if __name__ == "__main__":
    main()
