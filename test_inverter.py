import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock

@cocotb.test()
async def inverter_test(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    dut.a.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.y.value == 1, "Fail: 0 should become 1"

    dut.a.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.y.value == 0, "Fail: 1 should become 0"