% ==============================================================================
% Cognitive Entanglement - Dynamic Multi-Class Drone Trajectory Simulator
% Language: MATLAB (Simulink Compatible)
% Purpose: Performs numerical Integration (Runge-Kutta ODE45) of quadcopter
%          rigid-body dynamics. Dynamically scales physics equations based on
%          the input drone mass, dimensions, and moments of inertia.
%          Valid for all classes (80g Toy drones to 15kg heavy lifters).
% ==============================================================================

function simulate_trajectory(drone_mass, inertia_diag, max_thrust)
    clear; clc; close all;
    
    % Step 1: Handle dynamic mass arguments (Fallback to default if not supplied)
    if nargin < 1
        % Default: Custom 1.2kg DIY quadcopter parameters
        drone_mass = 1.2; 
        inertia_diag = [0.012, 0.012, 0.022];
        max_thrust = 32.0;
    end
    
    % Display aircraft physical class parameters
    fprintf('COGNITIVE ENTANGLEMENT: Simulating Dynamic Aircraft Class...\n');
    fprintf('Aircraft Mass: %.3f kg\n', drone_mass);
    fprintf('Moments of Inertia [Ixx, Iyy, Izz]: [%.4f, %.4f, %.4f] kg*m^2\n', ...
        inertia_diag(1), inertia_diag(2), inertia_diag(3));
    
    g = 9.81;            % Gravity (m/s^2)
    I = diag(inertia_diag); % Inertia Tensor (kg*m^2)
    
    % Time Span
    tspan = [0 10];      % 10 second flight simulation
    initial_state = zeros(12, 1); % [x, y, z, dx, dy, dz, phi, theta, psi, p, q, r]
    
    % Run numerical integration (Simulating Simulink continuous solver)
    [t, states] = ode45(@(t, y) drone_dynamics(t, y, drone_mass, g, I, max_thrust), tspan, initial_state);
    
    % Plot 3D Trajectory Profile
    figure('Color', [0.03 0.05 0.1]);
    plot3(states(:,1), states(:,2), -states(:,3), 'b-', 'LineWidth', 2);
    grid on; hold on;
    title(sprintf('Cognitive Entanglement - MATLAB 3D Flight Trajectory (%.2f kg Class)', drone_mass), 'Color', 'white');
    xlabel('East (meters)', 'Color', 'white');
    ylabel('North (meters)', 'Color', 'white');
    zlabel('Altitude (meters)', 'Color', 'white');
    set(gca, 'Color', [0.05 0.07 0.12], 'XColor', 'white', 'YColor', 'white', 'ZColor', 'white');
end

function dydt = drone_dynamics(t, y, m, g, I, max_thrust)
    % Extract states
    vel = y(4:6);  
    angles = y(7:9); 
    omega = y(10:12); 
    
    % Scale thrust output proportionally based on aircraft mass and max motor thrust
    T_hover = m * g;
    T = T_hover + (max_thrust - T_hover) * 0.1 * sin(t); % Oscillating thrust
    
    tau = [0.05 * sin(t); 0.02 * cos(t); 0.01 * sin(2*t)]; 
    
    % Compute Linear Acceleration: F = m * a
    R = rotation_matrix(angles);
    gravity_vec = [0; 0; g];
    thrust_vec = [0; 0; -T];
    accel = gravity_vec + (R * thrust_vec) / m;
    
    % Compute Angular Acceleration: M = I * alpha + omega x (I * omega)
    alpha = I \ (tau - cross(omega, I * omega));
    
    % Rate of change of Euler angles
    R_euler = [1, sin(angles(1))*tan(angles(2)), cos(angles(1))*tan(angles(2));
               0, cos(angles(1)),                 -sin(angles(1));
               0, sin(angles(1))/cos(angles(2)), cos(angles(1))/cos(angles(2))];
    d_angles = R_euler * omega;
    
    dydt = [vel; accel; d_angles; alpha];
end

function R = rotation_matrix(angles)
    phi = angles(1); theta = angles(2); psi = angles(3);
    R_x = [1 0 0; 0 cos(phi) -sin(phi); 0 sin(phi) cos(phi)];
    R_y = [cos(theta) 0 sin(theta); 0 1 0; -sin(theta) 0 cos(theta)];
    R_z = [cos(psi) -sin(psi) 0; sin(psi) cos(psi) 0; 0 0 1];
    R = R_z * R_y * R_x;
end
