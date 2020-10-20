.PHONY: prepare builddir benchdir run

BUILD_DIR=build
BENCH_DIR=bench

builddir:
	mkdir -p ${BUILD_DIR}

prepare: builddir
	cd ${BUILD_DIR} && git clone git@github.com:kaimast/kv-bench.git
	cd ${BUILD_DIR}/kv-bench && cargo build --release --features=all

benchdir:
	mkdir -p ${BENCH_DIR}

run: benchdir
	cd ${BENCH_DIR} && ../write_throughput.py --run --plot
