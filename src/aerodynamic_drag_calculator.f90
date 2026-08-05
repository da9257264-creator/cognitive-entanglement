! ==============================================================================
! Cognitive Entanglement - Aerodynamic Drag & Wind Shear Force Calculator
! Language: Fortran 90 (F90 Specification)
! Purpose: Performs lightning-fast double-precision array operations to calculate
!          the quadcopter's parasitic aerodynamic drag profiles under variable
!          high-speed wind velocity fields.
! ==============================================================================

program aerodynamic_drag_calculator
    implicit none

    ! Constant parameters
    double precision, parameter :: rho = 1.225d0      ! Air density at sea level (kg/m^3)
    double precision, parameter :: Cd = 1.15d0        ! Flat plate drag coefficient
    double precision, parameter :: frontal_area = 0.045d0 ! Frontal cross-sectional area (m^2)

    ! Variable declarations
    double precision :: wind_speed(3)                 ! Wind velocity components [Vx, Vy, Vz] (m/s)
    double precision :: drone_speed(3)                ! Drone velocity components [Vx, Vy, Vz] (m/s)
    double precision :: relative_speed(3)             ! Relative air velocity
    double precision :: speed_magnitude               ! Relative velocity magnitude
    double precision :: drag_force(3)                 ! Corrective drag vector [Fx, Fy, Fz] (Newtons)
    integer :: i

    ! Initialize relative velocities
    wind_speed = (/ 5.5d0, -2.0d0, 0.5d0 /)           ! Simulated wind vector
    drone_speed = (/ 2.0d0, 1.0d0, 0.0d0 /)           ! Command flight vector

    ! Step 1: Calculate relative velocity: V_rel = V_drone - V_wind
    do i = 1, 3
        relative_speed(i) = drone_speed(i) - wind_speed(i)
    end do

    ! Step 2: Compute velocity magnitude: ||V_rel|| = sqrt(Vx^2 + Vy^2 + Vz^2)
    speed_magnitude = dsqrt(sum(relative_speed**2))

    ! Step 3: Compute Aerodynamic Drag Force vector: F_drag = 0.5 * rho * Cd * Area * ||V_rel|| * V_rel
    do i = 1, 3
        drag_force(i) = 0.5d0 * rho * Cd * frontal_area * speed_magnitude * relative_speed(i)
    end do

    ! Display aerodynamic results
    print *, "COGNITIVE ENTANGLEMENT: Aerodynamic drag results calculated."
    print *, "Relative Speed Magnitude (m/s):", speed_magnitude
    print *, "Aerodynamic Drag Force Vector (Newtons):"
    print *, "F_drag_x:", drag_force(1)
    print *, "F_drag_y:", drag_force(2)
    print *, "F_drag_z:", drag_force(3)

end program aerodynamic_drag_calculator
