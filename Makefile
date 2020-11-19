.PHONY: prepare builddir benchdir run plot

BUILD_DIR=build
BENCH_DIR=bench

BACKENDS=lsm,leveldb

REPO=git@github.com:kaimast/kv-bench.git

builddir:
	mkdir -p ${BUILD_DIR}

prepare: builddir
	if [ ! -d ${BUILD_DIR}/kv-bench ]; then cd ${BUILD_DIR} && git clone ${REPO}; fi
	cd ${BUILD_DIR}/kv-bench && git pull && cargo update && cargo install --features=${BACKENDS} --path=.

benchdir:
	mkdir -p ${BENCH_DIR}

run: benchdir
	cd ${BENCH_DIR} && ../runner.py --run

plot: benchdir
	cd ${BENCH_DIR} && ../runner.py --plot
