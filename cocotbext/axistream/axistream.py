
""" Driver for AXI4-Stream protocol """

import cocotb
from cocotb.triggers import RisingEdge, ReadOnly
from cocotb.drivers import BusDriver
from cocotb.monitors import BusMonitor

from collections import namedtuple, deque

# pylint: disable=no-member
AXI4StreamFrame = namedtuple("AXI4StreamFrame", [
    "tid", "tdest", "tlast", "tkeep", "terr", "tdata"])


class AXI4StreamMaster(BusDriver):
    """AXI4-Stream Master
    """

    _signals = [
        "tvalid", "tready", "tid", "tdest",
        "tlast", "tkeep", "terr", "tdata"]

    def __init__(self, entity, name, clock, **kwargs):
        BusDriver.__init__(self, entity, name, clock, **kwargs)

        # defaults
        self.bus.tvalid.setimmediatevalue(0)
        self.bus.tid.setimmediatevalue(0)
        self.bus.tdest.setimmediatevalue(0)
        self.bus.tlast.setimmediatevalue(0)
        self.bus.tkeep.setimmediatevalue(0)
        self.bus.terr.setimmediatevalue(0)
        self.bus.tdata.setimmediatevalue(0)

    async def write(self, frame, timeout=None):
        self.bus.tvalid <= 1
        self.bus.tid <= frame.tid
        self.bus.tdest <= frame.tdest
        self.bus.tlast <= frame.tlast
        self.bus.tkeep <= frame.tkeep
        self.bus.terr <= frame.terr
        self.bus.tdata <= frame.tdata

        while True:
            await ReadOnly()
            if self.bus.tready.value or timeout == 0:
                break
            if timeout is not None:
                timeout -= 1
            await RisingEdge(self.clock)
        if timeout == 0:
            return False
        await RisingEdge(self.clock)
        self.bus.tvalid <= 0
        return True

class AXI4StreamMonitor(BusMonitor):
    """AXI4-Stream Monitor
    """

    _signals = [
        "tvalid", "tready", "tid", "tdest",
        "tlast", "tkeep", "terr", "tdata"]

    def __init__(self, entity, name, clock, **kwargs):
        BusMonitor.__init__(self, entity, name, clock, **kwargs)

    async def _monitor_recv(self):
        while True:
            await ReadOnly()
            if self.bus.tvalid.value and self.bus.tready.value:
                self._recv(AXI4StreamFrame(
                    int(self.bus.tid),
                    int(self.bus.tdest),
                    int(self.bus.tlast),
                    int(self.bus.tkeep),
                    int(self.bus.terr),
                    int(self.bus.tdata)
                ))
            await RisingEdge(self.clock)
