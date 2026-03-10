import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock

@cocotb.test()
async def counter_test(dut):
    # 1. Start the Clock
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # 2. Reset the Hardware
    dut.reset_n.value = 0
    dut.en.value = 0
    await RisingEdge(dut.clk)
    dut.reset_n.value = 1  # Release reset
    
    # 3. Test: Does it count when enabled?
    dut.en.value = 1
    for i in range(5):
        await RisingEdge(dut.clk)
        await Timer(1,units="ns")
        dut._log.info(f"Cycle {i}: Count is {int(dut.count.value)}")
    
    # 4. Test: Does it pause when disabled?
   # 4. Test: Does it pause when disabled?
    await RisingEdge(dut.clk)
    dut.en.value = 0

    await Timer(1,units="ns")
    current_val = int(dut.count.value) # Store current value as integer
    dut._log.info(f"Counter stopped at: {current_val}")

    await RisingEdge(dut.clk)          # Wait for the clock to strike
    await Timer(1, units="ns")         # NEW: Wait 1ns for logic to settle!
    
    # extra_val=current_val
    # dut._log.info(f"Counter extra value at: {extra_val}")

    actual_val= int(dut.count.value)
    assert actual_val == current_val, f"Error: Expected {current_val}, got {actual_val}"
    dut._log.info("SUCCESS : counter stayed still while disabled")