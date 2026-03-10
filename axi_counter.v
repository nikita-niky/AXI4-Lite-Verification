module axi_counter (
    input  wire        aclk,
    input  wire        aresetn,
    // Read Address Channel
    input  wire [31:0] araddr,
    input  wire        arvalid,
    output reg         arready,
    // Read Data Channel
    output reg  [31:0] rdata,
    output reg         rvalid,
    input  wire        rready
);
    // Internal 4-bit counter logic
    reg [3:0] count_reg;
    always @(posedge aclk or negedge aresetn) begin
        if (!aresetn) count_reg <= 4'b0;
        else          count_reg <= count_reg + 1'b1;
    end

    // AXI-Lite Read Logic (Simplified Handshake)
    always @(posedge aclk or negedge aresetn) begin
        if (!aresetn) begin
            arready <= 1'b0;
            rvalid  <= 1'b0;
            rdata   <= 32'b0;
        end else begin
            // 1. Accept Address
            arready <= 1'b1; 
            
            // 2. When Address is Valid, Send Data
            if (arvalid && arready) begin
                rdata  <= {28'b0, count_reg}; // Put counter value in data bus
                rvalid <= 1'b1;
            end 
            
            // 3. Complete Handshake
            if (rvalid && rready) begin
                rvalid <= 1'b0;
            end
        end
    end

    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, axi_counter);
    end
endmodule