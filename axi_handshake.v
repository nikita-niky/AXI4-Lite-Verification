module axi_counter (
    input  wire        aclk,
    input  wire        aresetn,
    // Write Address Channel
    input  wire [31:0] awaddr,
    input  wire        awvalid,
    output reg         awready,
    // Write Data Channel
    input  wire [31:0] wdata,
    input  wire        wvalid,
    output reg         wready,
    // Read Address Channel
    input  wire [31:0] araddr,
    input  wire        arvalid,
    output reg         arready,
    // Read Data Channel
    output reg  [31:0] rdata,
    output reg         rvalid,
    input  wire        rready
);
    // 4-bit internal counter
    reg [3:0] count_reg;

    // Combined AXI-Lite Logic
    always @(posedge aclk or negedge aresetn) begin
        if (!aresetn) begin
            count_reg <= 4'b0;
            awready <= 1'b0;
            wready  <= 1'b0;
            arready <= 1'b0;
            rvalid  <= 1'b0;
            rdata   <= 32'b0;
        end else begin
            // --- WRITE LOGIC (Slave is always ready) ---
            awready <= 1'b1;
            wready  <= 1'b1;

            if (awvalid && awready && wvalid && wready) begin
                count_reg <= wdata[3:0]; // Load counter from Bus
            end else begin
                count_reg <= count_reg + 1'b1; // Default: Increment
            end

            // --- READ LOGIC ---
            arready <= 1'b1;
            if (arvalid && arready) begin
                rdata  <= {28'b0, count_reg};
                rvalid <= 1'b1;
            end 
            
            // Clear RVALID once Master acknowledges (RREADY)
            if (rvalid && rready) begin
                rvalid <= 1'b0;
            end
        end
    end

    // Standard for simulation viewing
    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, axi_counter);
    end
endmodule