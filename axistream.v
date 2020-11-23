`timescale 1ns/1ps

module axistream(
    input clk,

    // slave interface
    input s_axis_tvalid,
    output s_axis_tready,
    input s_axis_tid,
    input s_axis_tdest,
    input s_axis_tlast,
    input s_axis_tkeep,
    input s_axis_terr,
    input [7:0] s_axis_tdata,

    // master interface
    output m_axis_tvalid,
    input m_axis_tready,
    output m_axis_tid,
    output m_axis_tdest,
    output m_axis_tlast,
    output m_axis_tkeep,
    output m_axis_terr,
    output [7:0] m_axis_tdata
);

    // simple passthrough
    assign m_axis_tvalid = s_axis_tvalid;
    assign s_axis_tready = m_axis_tready;
    assign m_axis_tid = s_axis_tid;
    assign m_axis_tdest = s_axis_tdest;
    assign m_axis_tlast = s_axis_tlast;
    assign m_axis_tkeep = s_axis_tkeep;
    assign m_axis_terr = s_axis_terr;
    assign m_axis_tdata = s_axis_tdata;

    `ifdef COCOTB_SIM
    initial begin
    $dumpfile("axistream.vcd");
    $dumpvars(0, axistream);
    #1;
    end
    `endif

endmodule
