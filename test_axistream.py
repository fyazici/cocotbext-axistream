import random
import cocotb
import cocotb.scoreboard
from cocotb.clock import Clock
from cocotb.drivers import BitDriver
from cocotb.generators.bit import intermittent_single_cycles

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

    sb = cocotb.scoreboard.Scoreboard(dut)
    sb.add_interface(monitor_2, expected_out)
    
    dut.m_axis_tready <= 1

    for _ in range(10):
        val = random.randint(0, 100)
        m_frame = AXI4StreamFrame(0, 1, 1, 1, 0, val)
        await master.write(m_frame)
    
    raise sb.result
        

