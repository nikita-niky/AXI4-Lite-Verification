import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock

class AXIDriver:
    """A professional Driver to handle AXI-Lite Protocol signaling"""
    def __init__(self, dut):
        self.dut = dut

    async def write(self, address, value):
        """Perform an AXI-Lite Write transaction"""
        self.dut.awaddr.value = address
        self.dut.awvalid.value = 1
        self.dut.wdata.value = value
        self.dut.wvalid.value = 1
        
        await RisingEdge(self.dut.aclk)
        while not (int(self.dut.awready.value) and int(self.dut.wready.value)):
            await RisingEdge(self.dut.aclk)
            
        await Timer(1, "ns") # Settle time
        self.dut.awvalid.value = 0
        self.dut.wvalid.value = 0

    async def read(self, address):
        """Perform an AXI-Lite Read transaction"""
        self.dut.araddr.value = address
        self.dut.arvalid.value = 1
        self.dut.rready.value = 1
        
        await RisingEdge(self.dut.aclk)
        while int(self.dut.rvalid.value) == 0:
            await RisingEdge(self.dut.aclk)
            
        data = int(self.dut.rdata.value)
        self.dut.arvalid.value = 0
        return data

@cocotb.test()
async def full_system_verify(dut):
    # 1. Start Clock (100MHz)
    cocotb.start_soon(Clock(dut.aclk, 10, units="ns").start())
    driver = AXIDriver(dut)

    # 2. Global Reset
    dut.aresetn.value = 0
    await Timer(20, "ns")
    dut.aresetn.value = 1
    await RisingEdge(dut.aclk)

    # 3. Test Write: Load the counter with '10'
    dut._log.info("Test Step 1: Loading counter with value 10...")
    await driver.write(0x0, 10)

    # 4. Wait 2 clock cycles to let it increment (10 -> 11 -> 12)
    await RisingEdge(dut.aclk)
    await RisingEdge(dut.aclk)

    # 5. Test Read: Verify it reached '12'
    val = await driver.read(0x0)
    dut._log.info(f"Test Step 2: Read back counter value: {val}")

    assert val == 12, f"Verification Failed! Expected 12, got {val}"
    dut._log.info("### SUCCESS: AXI READ/WRITE VERIFIED ###")