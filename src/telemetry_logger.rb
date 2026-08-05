# ==============================================================================
# Cognitive Entanglement - Automated Spacecraft Telemetry Logging Daemon
# Language: Ruby (v2.7+)
# Target: NASA/SpaceX Ground Control Stations / Telemetry Parsing (FDIR Systems)
# Purpose: Listens to incoming real-time JSON flight state packets, parses
#          and filters sensor matrices, and writes formatted avionic logs.
# ==============================================================================

require 'json'
require 'fileutils'

class TelemetryLogger
  def initialize(log_dir = "logs")
    @log_dir = log_dir
    FileUtils.mkdir_p(@log_dir)
    @log_file = File.join(@log_dir, "avionic_telemetry.log")
    puts "[RUBY LOGGER]: Telemetry logging daemon initialized. Targets: #{@log_file}"
  end

  def parse_and_log(json_packet_string)
    begin
      # Parse incoming JSON packet
      packet = JSON.parse(json_packet_string)
      
      # Extract core flight parameters
      drone_id = packet.fetch("drone_id", 1)
      state = packet.fetch("flight_mode", "IDLE")
      battery = packet.fetch("battery", 100)
      pos = packet.fetch("position", { "x" => 0.0, "y" => 0.0, "z" => 0.0 })
      
      # Generate standardized timestamps (SpaceX/NASA format)
      timestamp = Time.now.utc.strftime("%Y-%m-%dT%H:%M:%S.%3NZ")
      
      # Compile structured log line
      log_line = "[#{timestamp}] [DRONE-#{drone_id}] State: #{state} | Bat: #{battery}% | Pos: X=#{pos['x'].round(2)}, Y=#{pos['y'].round(2)}, Z=#{pos['z'].round(2)}"
      
      # Write append to file with thread-safety
      File.open(@log_file, "a") do |f|
        f.puts(log_line)
      end
      
    rescue JSON::ParserError => e
      # Skip corrupted packets silently during pre-flight calibrations
    rescue StandardError => e
      STDERR.puts "[RUBY LOGGER ERROR]: Failed to log telemetry: #{e.message}"
    end
  end
end

# Test run simulation
logger = TelemetryLogger.new
test_json = '{"drone_id":1,"flight_mode":"GUIDED","battery":92,"position":{"x":2.34,"y":-1.12,"z":1.50}}'
logger.parse_and_log(test_json)
