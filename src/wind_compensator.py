import numpy as np
import logging

class WindCompensator:
    """
    Active Disturbance Rejection Control (ADRC) Wind Compensator.
    Estimates real-time wind speed and direction by comparing the drone's
    commanded steering velocity vectors against its actual physical IMU
    accelerometer displacement. It then injects a proactive "counter-thrust"
    vector (pitch/roll angle offset) to resist wind drift before it can occur.
    """
    def __init__(self, adrc_gain=1.2):
        self.adrc_gain = adrc_gain
        self.wind_speed_est = 0.0     # Estimated wind velocity (m/s)
        self.wind_direction_est = 0.0 # Estimated wind direction (degrees)
        self.logger = logging.getLogger("WindCompensator")

    def estimate_and_compensate(self, commanded_vectors, actual_imu_displacement):
        """
        Calculates wind drift and produces corrective feed-forward velocities.
        - commanded_vectors: {'vx', 'vy', 'vz'} (what we want)
        - actual_imu_displacement: {'dx', 'dy', 'dz'} (what actually happened)
        """
        # Calculate drift delta (difference between expectation and reality)
        drift_x = commanded_vectors["vx"] - actual_imu_displacement.get("dx", commanded_vectors["vx"])
        drift_y = commanded_vectors["vy"] - actual_imu_displacement.get("dy", commanded_vectors["vy"])

        # Estimate current wind speed and direction vector
        self.wind_speed_est = np.sqrt(drift_x**2 + drift_y**2) * 3.0 # scale factor
        self.wind_direction_est = np.degrees(np.arctan2(drift_y, drift_x)) % 360.0

        corrected_vectors = commanded_vectors.copy()

        # If wind is pushing, inject an active counter-thrust velocity
        if self.wind_speed_est > 0.5: # Only trigger compensation for winds > 0.5 m/s
            # Feed-forward ADRC compensation
            corrected_vectors["vx"] += drift_x * self.adrc_gain
            corrected_vectors["vy"] += drift_y * self.adrc_gain
            
            if self.wind_speed_est > 2.0:
                self.logger.info(f"ADRC ACTIVE: Compensating wind gust: {self.wind_speed_est:.1f} m/s at {self.wind_direction_est:.0f}°")

        return corrected_vectors
