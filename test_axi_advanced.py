import cocotb
import random
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock

class AXIDriver:
    def __init__(self, dut):
        self.dut = dut

    async def read_address(self, address):
        """A professional function to handle an AXI Read"""
        self.dut.araddr.value = address
        self.dut.arvalid.value = 1
        self.dut.rready.value = 1
        
        await RisingEdge(self.dut.aclk)
        while int(self.dut.rvalid.value) == 0:
            await RisingEdge(self.dut.aclk)
            
        data = int(self.dut.rdata.value)
        self.dut.arvalid.value = 0
        return data

# @cocotb.test()
# async def advanced_test(dut):
#     cocotb.start_soon(Clock(dut.aclk, 10, units="ns").start())
    
#     # Reset
#     dut.aresetn.value = 0
#     await Timer(20, "ns")
#     dut.aresetn.value = 1
    
#     # Use our new Driver!
#     driver = AXIDriver(dut)
    
#     for i in range(3):
#         await Timer(50, "ns") # Wait for counter to move
#         val = await driver.read_address(0x0)
#         dut._log.info(f"READ {i}: Captured value {val}")

@cocotb.test()
async def stress_test(dut):
    cocotb.start_soon(Clock(dut.aclk, 10, units="ns").start())
    
    # Reset
    dut.aresetn.value = 0
    await Timer(20, "ns")
    dut.aresetn.value = 1
    
    driver = AXIDriver(dut)
    
    dut._log.info("Starting Stress Test: 1000 AXI Reads")

    for i in range(1000):
        # Professional tip: Add a small random delay between reads
        # This checks if your 'rvalid' logic handles pauses correctly
        delay = random.randint(1, 5)
        for _ in range(delay):
            await RisingEdge(dut.aclk)

        val = await driver.read_address(0x0)
        
        # We don't want to log 1000 lines, so only log every 100th
        if i % 100 == 0:
            dut._log.info(f"Transaction {i}: Received Counter Value {val}")

    dut._log.info("STRESS TEST COMPLETE: 1000 Transactions Successful!")