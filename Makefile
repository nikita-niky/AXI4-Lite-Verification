SIM ?= icarus
TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES += axi_handshake.v
TOPLEVEL = axi_counter
MODULE = test_axi_handshake
include $(shell cocotb-config --makefiles)/Makefile.sim