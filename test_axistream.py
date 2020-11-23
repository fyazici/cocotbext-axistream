import random
import cocotb
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

    actual_out = []
    expected_out = []

    master = AXI4StreamMaster(dut, "s_axis", dut.clk)

    # pylint: disable=unused-variable
    monitor = AXI4StreamMonitor(dut, "m_axis", dut.clk)
    monitor.add_callback(lambda frame: actual_out.append(frame))
    
    dut.m_axis_tready <= 1

    for _ in range(10):
        val = random.randint(0, 100)
        m_frame = AXI4StreamFrame(0, 1, 1, 1, 0, val)
        expected_out.append(m_frame)
        await master.write(m_frame)
    
    assert actual_out == expected_out, "outputs did not match {} vs {}".format(actual_out, expected_out)
        

