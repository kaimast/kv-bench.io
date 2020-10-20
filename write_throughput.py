#! /usr/bin/python3

import argparse

from subprocess import call

BIN_PATH="../build/kv_bench/target/release/kv_bench"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true", default=False)
    parser.add_argument("--plot", action="store_true", default=False)

    args = parser.parse_args()

    if args.run:
        run()

def run():
    batch_sizes = [1, 100, 1000, 10000]

    for batch_size in batch_sizes:
        call([BIN_PATH])

if __name__ == "__main__":
    main()
