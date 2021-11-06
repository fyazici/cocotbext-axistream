import random
import cocotb
import cocotb_bus.scoreboard
from cocotb.clock import Clock
from cocotb_bus.drivers import BitDriver

from cocotbext.axistream import *
import itertools

@cocotb.test()
async def test_axistream_passthrough(dut):
    """ Test that AXI4Stream Master-Slave communication """

    clock = Clock(dut.clk, 10, units="ns")
    cocotb.fork(clock.start())

    expected_out = []

    master = AXI4StreamMaster(dut, "s_axis", dut.clk)

    monitor_1 = AXI4StreamMonitor(dut, "s_axis", dut.clk)
    monitor_1.add_callback(lambda frame: expected_out.append(frame))
    monitor_2 = AXI4StreamMonitor(dut, "m_axis", dut.clk)

    sb = cocotb_bus.scoreboard.Scoreboard(dut)
    sb.add_interface(monitor_2, expected_out)
    
    dut.m_axis_tready.value = 1

    for _ in range(10):
        val = random.randint(0, 100)
        m_frame = AXI4StreamFrame(0, 1, 1, 1, 0, val)
        if _ == 5:
            dut.m_axis_tready.value = 0
        r = await master.write(m_frame, 3)
        assert r, "write timed out"
    
    raise sb.result
        

