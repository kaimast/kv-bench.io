#! /usr/bin/python3

import argparse
import json
import matplotlib.pyplot as plt
import numpy as np

from pandas import DataFrame, read_csv
from subprocess import call

BIN_PATH = "kv-bench"
OUT_FILE = "data.json"
RESULTS = "results.csv"

BACKENDS = ["leveldb", "rocksdb", "lsm"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true", default=False)
    parser.add_argument("--plot", action="store_true", default=False)

    args = parser.parse_args()

    if args.run:
        run()

    if args.plot:
        plot()

def run():
    workload = "write_only"
    batch_sizes = [1, 100, 1000, 10000]
    total_ops = 50000

    columns = ["backend", "batch_size", "throughput"]
    results = DataFrame([], columns=columns)

    num_iterations = 5
    num_runs = len(BACKENDS) * len(batch_sizes) * num_iterations
    count = 0

    for backend in BACKENDS:
        for batch_size in batch_sizes:
            for _ in range(num_iterations):
                num_ops = int(total_ops / batch_size)

                call([BIN_PATH, "--backend="+backend, "--workload="+workload, "--batch_size=%i"%batch_size,
                    "--sync=true", "--outfile="+OUT_FILE, "--num_ops=%i"%num_ops])

                with open(OUT_FILE) as jfile:
                    data = json.load(jfile)

                print(str(data))

                row = DataFrame([[backend, batch_size, data["throughput"]]], columns=columns)
                results = results.append(row)

                results.to_csv(RESULTS, index=False)

                count += 1
                print("Progress: %i out of %i" % (count, num_runs))

    print("Done")

def plot():
    df = read_csv(RESULTS)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for (pos, backend) in enumerate(BACKENDS):
        data = df[df["backend"] == backend]
        keys = data.batch_size.unique()
        means = []
        sdevs = []

        for batch_size in keys:
            vals = data[data["batch_size"] == batch_size]
            tpt = vals.throughput / (1000*1000)
            means.append(np.mean(tpt))
            sdevs.append(np.std(tpt))

        widths = 0.5*keys
        ax.bar(keys + pos*widths, means, yerr=sdevs, label=backend, width=widths)

    ax.set_xlabel("batch size")
    ax.set_ylabel("throughput (MB/s)")
    ax.set_xscale('log')

    plt.tight_layout()
    fig.legend()
    fig.savefig("results.pdf")

if __name__ == "__main__":
    main()
