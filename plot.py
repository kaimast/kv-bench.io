#! /usr/bin/python3

import argparse
from pandas import read_csv

import numpy as np
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, default="results.csv")

    args = parser.parse_args()

    data = read_csv(args.filename)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    backends = data.backend.unique()
    workloads = data.workload.unique()
    yticks = np.array([i for i in range(len(workloads))])

    for (pos, backend) in enumerate(backends):
        bdata = data[data["backend"] == backend]
        means = []
        sdevs = []

        for workload in workloads:
            wdata = bdata[bdata["workload"] == workload]

            tpt = wdata.throughput / (1000*1000)
            means.append(np.mean(tpt))
            sdevs.append(np.std(tpt))

        width = 1.0/(len(backends)+2)
        ax.bar(yticks + pos*width, means, yerr=sdevs, label=backend, width=width)

    ax.set_ylabel("throughput (MB/s)")

    ax.set_xlabel("workload")
    ax.set_xticks(yticks)
    ax.set_xticklabels(workloads)

    plt.tight_layout()
    fig.legend()
    fig.savefig("results.pdf")

if __name__ == "__main__":
    main()
