module inverter (
    input wire clk,
    input wire a,
    output reg y
);
    always @(posedge clk) begin
        y <= ~a;
    end

    // This block creates the waveform file
    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, inverter);
    end
endmodule