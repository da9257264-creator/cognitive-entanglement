------------------------------------------------------------------------------
-- Cognitive Entanglement - FPGA Optical Encoder Position Decoder
-- Language: VHDL (IEEE 1076 Specification)
-- Target: Space-Grade Rad-Hard FPGAs (NASA & Lockheed Martin Avionics)
-- Purpose: Implements an asynchronous Quadrature Decoder to read physical
--          motor shaft encoders for sub-micrometer positioning precision.
------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity optical_encoder is
    Port (
        clk          : in  STD_LOGIC; -- System clock
        rst_n        : in  STD_LOGIC; -- Active-low reset
        encoder_a    : in  STD_LOGIC; -- Encoder Phase A input
        encoder_b    : in  STD_LOGIC; -- Encoder Phase B input
        position_out : out STD_LOGIC_VECTOR(15 downto 0) -- 16-bit decoded shaft position
    );
end optical_encoder;

architecture Behavioral of optical_encoder is
    signal enc_a_reg : STD_LOGIC_VECTOR(1 downto 0) := "00";
    signal enc_b_reg : STD_LOGIC_VECTOR(1 downto 0) := "00";
    signal count_reg : signed(15 downto 0) := (others => '0');
begin

    -- Dual-stage shift registers for clock boundary synchronization and de-glitching
    process(clk, rst_n)
    begin
        if rst_n = '0' then
            enc_a_reg <= "00";
            enc_b_reg <= "00";
            count_reg <= (others => '0');
        elsif rising_edge(clk) then
            enc_a_reg <= enc_a_reg(0) & encoder_a;
            enc_b_reg <= enc_b_reg(0) & encoder_b;

            -- Quadrature Decoder state logic
            if (enc_a_reg(1) = '0' and enc_a_reg(0) = '1') then -- Phase A rising edge
                if enc_b_reg(1) = '0' then
                    count_reg <= count_reg + 1; -- Clockwise rotation
                else
                    count_reg <= count_reg - 1; -- Counter-clockwise rotation
                end if;
            end if;
        end if;
    end process;

    position_out <= std_logic_vector(count_reg);

end Behavioral;
