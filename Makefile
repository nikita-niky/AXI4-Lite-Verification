SIM ?= icarus
TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES += axi_counter.v
TOPLEVEL = axi_counter
MODULE = test_axi
include $(shell cocotb-config --makefiles)/Makefile.sim