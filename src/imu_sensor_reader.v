// ==============================================================================
// Cognitive Entanglement - FPGA SPI Hardware Register IMU Sensor Reader
// Language: Verilog (IEEE 1364 Specification)
// Target: Space-Grade Rad-Hard FPGAs (Xilinx / Altera hardware layer)
// Purpose: Implements an asynchronous Serial Peripheral Interface (SPI) receiver
//          to pull raw 16-bit accelerometer and gyroscope registers straight
//          from physical sensor chips with zero-latency.
// ==============================================================================

module imu_sensor_reader (
    input  wire        clk,        // System master clock
    input  wire        rst_n,      // Asynchronous active-low reset
    input  wire        spi_miso,   // Master-In Slave-Out serial line
    output reg         spi_mosi,   // Master-Out Slave-In serial line
    output reg         spi_sck,    // SPI serial clock line
    output reg         spi_cs_n,   // SPI active-low chip select
    output reg [15:0]  sensor_data,// 16-bit compiled register sensor outputs
    output reg         data_valid  // High pulse indicating transaction complete
);

    // SPI State Machine registers
    localparam STATE_IDLE  = 2'b00;
    localparam STATE_START = 2'b01;
    localparam STATE_SHIFT = 2'b10;
    localparam STATE_DONE  = 2'b11;

    reg [1:0]  state, next_state;
    reg [3:0]  bit_counter;
    reg [15:0] shift_reg;
    reg [7:0]  clk_divider;

    // Clock divider to generate SPI SCK from system master clock
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            clk_divider <= 8'h00;
            spi_sck     <= 1'b0;
        end else begin
            clk_divider <= clk_divider + 1'b1;
            if (clk_divider == 8'h0F) begin
                clk_divider <= 8'h00;
                spi_sck     <= ~spi_sck;
            end
        end
    end

    // SPI Transaction State Machine
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= STATE_IDLE;
        end else begin
            state <= next_state;
        end
    end

    always @(*) begin
        next_state = state;
        case (state)
            STATE_IDLE: begin
                if (rst_n) next_state = STATE_START;
            end
            STATE_START: begin
                next_state = STATE_SHIFT;
            end
            STATE_SHIFT: begin
                if (bit_counter == 4'hF && clk_divider == 8'h00 && spi_sck)
                    next_state = STATE_DONE;
            end
            STATE_DONE: begin
                next_state = STATE_IDLE;
            end
        endcase
    end

    // SPI Shift Register and Bit Counter
    always @(posedge spi_sck or negedge rst_n) begin
        if (!rst_n) begin
            bit_counter <= 4'h0;
            shift_reg   <= 16'h0000;
            spi_cs_n    <= 1'b1;
            data_valid  <= 1'b0;
            sensor_data <= 16'h0000;
        end else begin
            case (state)
                STATE_START: begin
                    spi_cs_n    <= 1'b0; // Activate chip select
                    bit_counter <= 4'h0;
                    data_valid  <= 1'b0;
                end
                STATE_SHIFT: begin
                    shift_reg   <= {shift_reg[14:0], spi_miso}; // Shift in bits
                    bit_counter <= bit_counter + 1'b1;
                end
                STATE_DONE: begin
                    spi_cs_n    <= 1'b1; // Release chip select
                    sensor_data <= shift_reg;
                    data_valid  <= 1'b1; // Trigger data valid pulse
                end
            endcase
        end
    end

endmodule
