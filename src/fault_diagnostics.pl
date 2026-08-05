% ==============================================================================
% Cognitive Entanglement - Autonomous Avionics Fault Diagnosis Expert System
% Language: Prolog (ISO Prolog Specification)
% Target: NASA Deep-Space Autonomous Reasoning & Fault Isolation (FDIR) Systems
% Purpose: Implements first-order predicate logic rules to identify, classify,
%          and isolate systemic thermal, power, and actuator failures on-the-fly.
% ==============================================================================

% ----------------------------------------------------
% 1. System Telemetry Declarations (Facts)
% ----------------------------------------------------
sensor_reading(motor_1, temperature, 85).  % Motor 1 temperature in Celsius
sensor_reading(motor_1, current, 45).      % Motor 1 current in Amperes
sensor_reading(battery, voltage, 11.2).     % Battery voltage in Volts
sensor_reading(battery, temperature, 48).  % Battery temperature in Celsius
sensor_reading(webrtc_link, signal, 12).   % WebRTC RSSI signal strength

% ----------------------------------------------------
% 2. Safety Limit Declarations
% ----------------------------------------------------
threshold_limit(motor, temperature, 80).    % Max safe motor temp
threshold_limit(motor, current, 40).        % Max safe motor current draw
threshold_limit(battery, voltage, 11.5).    % Min safe battery voltage
threshold_limit(battery, temperature, 45).  % Max safe battery temp
threshold_limit(webrtc_link, signal, 15).   % Min safe RSSI signal

% ----------------------------------------------------
% 3. First-Order Logic Diagnostics Rules
% ----------------------------------------------------

% Rule A: Classify direct sensor violations
anomaly_detected(Component, Parameter, Value) :-
    sensor_reading(Component, Parameter, Value),
    threshold_limit(Component, Parameter, Limit),
    Parameter = temperature, Value > Limit.

anomaly_detected(Component, Parameter, Value) :-
    sensor_reading(Component, Parameter, Value),
    threshold_limit(Component, Parameter, Limit),
    Parameter = current, Value > Limit.

anomaly_detected(Component, Parameter, Value) :-
    sensor_reading(Component, Parameter, Value),
    threshold_limit(Component, Parameter, Limit),
    Parameter = voltage, Value < Limit.

anomaly_detected(Component, Parameter, Value) :-
    sensor_reading(Component, Parameter, Value),
    threshold_limit(Component, Parameter, Limit),
    Parameter = signal, Value < Limit.

% Rule B: Infer complex systemic failures (Sensor Fusion)
system_failure(battery_thermal_runaway) :-
    anomaly_detected(battery, temperature, _),
    anomaly_detected(battery, voltage, _).

system_failure(motor_actuator_jam) :-
    anomaly_detected(Component, temperature, _),
    anomaly_detected(Component, current, _),
    atom_concat(motor_, _, Component).

system_failure(telemetry_link_loss) :-
    anomaly_detected(webrtc_link, signal, _).

% Rule C: Formulate corrective FDIR mitigation action directives
corrective_action_required(force_emergency_landing) :-
    system_failure(battery_thermal_runaway).

corrective_action_required(trigger_failsafe_hover) :-
    system_failure(telemetry_link_loss).

corrective_action_required(reduce_throttle_on_component(Component)) :-
    system_failure(motor_actuator_jam),
    sensor_reading(Component, current, _).
