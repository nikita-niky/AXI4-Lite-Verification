import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock

@cocotb.test()
async def axi_read_test(dut):
    # Setup Clock
    cocotb.start_soon(Clock(dut.aclk, 10, units="ns").start())

    # Reset
    dut.aresetn.value = 0
    dut.arvalid.value = 0
    dut.rready.value = 0
    await RisingEdge(dut.aclk)
    await Timer(1, units="ns")
    dut.aresetn.value = 1
    
    # Wait for counter to run a bit
    for _ in range(5): await RisingEdge(dut.aclk)

    # --- START AXI READ TRANSACTION ---
    dut._log.info("Starting AXI Read...")
    dut.araddr.value = 0x0000  # Address doesn't matter for this simple version
    dut.arvalid.value = 1
    dut.rready.value = 1     # "CPU" is ready to receive
    
    await RisingEdge(dut.aclk)
    await Timer(1, units="ns")
    
    # Check if data is valid
    while int(dut.rvalid.value) == 0:
        await RisingEdge(dut.aclk)
    
    captured_data = int(dut.rdata.value)
    dut._log.info(f"AXI Read Success! Counter value received: {captured_data}")
    
    # Cleanup
    dut.arvalid.value = 0
    await RisingEdge(dut.aclk)