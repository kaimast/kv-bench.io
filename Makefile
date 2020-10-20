.PHONY: prepare builddir benchdir run plot

BUILD_DIR=build
BENCH_DIR=bench

REPO=git@github.com:kaimast/kv-bench.git

builddir:
	mkdir -p ${BUILD_DIR}

prepare: builddir
	if [ ! -d ${BUILD_DIR}/kv-bench ]; then cd ${BUILD_DIR} && git clone ${REPO}; fi
	cd ${BUILD_DIR}/kv-bench && git pull && cargo install --features=all --path=.

benchdir:
	mkdir -p ${BENCH_DIR}

run: benchdir
	cd ${BENCH_DIR} && ../write_throughput.py --run

plot: benchdir
	cd ${BENCH_DIR} && ../write_throughput.py --plot
