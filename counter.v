module counter (
    input  wire clk,      // The heartbeat
    input  wire reset_n,  // Active-low reset (0 = start over)
    input  wire en,       // Enable (1 = count, 0 = pause)
    output reg [3:0] count // 4-bit output (0000 to 1111)
);

    // This block triggers every time the clock goes from 0 to 1
    always @(posedge clk or negedge reset_n) begin
        if (!reset_n) begin
            count <= 4'b0000; // If reset is 0, set count to zero
        end else if (en) begin
            count <= count + 1'b1; // If enabled, add 1
        end
        // If en is 0, it just keeps its current value!
    end

    // Standard lines to see waveforms
    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, counter);
    end
endmodule