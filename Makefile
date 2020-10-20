.PHONY: prepare

BUILD_DIR=build

prepare:
	mkdir -p ${BUILD_DIR}
	cd ${BUILD_DIR} && git clone git@github.com:kaimast/kv-bench.git
	cd ${BUILD_DIR}/kv-bench && cargo build --release --features=all
