import argparse
from pandas import read_csv

import numpy as np
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, default="results.csv")

    args = parser.parse_args()

    df = read_csv(filename)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    backends = df.backends.unique()
    workloads = df.workloads.unique()

    for workload in workloads:
        wdata = df[df["workload"] == workload]

        for (pos, backend) in enumerate(backends):
            data = wdata[wdata["backend"] == backend]
            vals = data[0]
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
