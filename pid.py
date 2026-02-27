import time
import numpy as np


class FlightPID:
    def __init__(self,
                 kp=0.0025,
                 ki=0.0008,
                 kd=0.0012,
                 max_output=300,
                 deadband=5,
                 integral_limit=300,
                 max_rate_change=40):

        # PID Gains
        self.kp = kp
        self.ki = ki
        self.kd = kd

        # Limits
        self.max_output = max_output
        self.deadband = deadband
        self.integral_limit = integral_limit
        self.max_rate_change = max_rate_change

        # Internal states
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_derivative = 0.0
        self.prev_output = 0.0

        self.last_time = time.time()

    def reset(self):
        """Reset PID states"""
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_derivative = 0.0
        self.prev_output = 0.0
        self.last_time = time.time()

    def update(self, error):

        current_time = time.time()
        dt = current_time - self.last_time

        # Fixed timestep protection
        if dt <= 0 or dt > 0.1:
            dt = 0.02

        self.last_time = current_time

        # Deadband (center stability)
        if abs(error) < self.deadband:
            error = 0.0

        # --- PROPORTIONAL ---
        p = self.kp * error

        # --- INTEGRAL (anti-windup) ---
        self.integral += error * dt
        self.integral = np.clip(self.integral,
                                -self.integral_limit,
                                self.integral_limit)
        i = self.ki * self.integral

        # --- DERIVATIVE (smoothed) ---
        derivative = (error - self.prev_error) / dt

        # Low-pass filter derivative
        derivative = 0.7 * self.prev_derivative + 0.3 * derivative

        d = self.kd * derivative

        self.prev_error = error
        self.prev_derivative = derivative

        # --- RAW OUTPUT ---
        output = p + i + d

        # Soft clamp
        output = np.clip(output,
                         -self.max_output,
                         self.max_output)

        # --- RATE LIMITER (servo jerk prevention) ---
        delta = output - self.prev_output
        delta = np.clip(delta,
                        -self.max_rate_change,
                        self.max_rate_change)

        output = self.prev_output + delta
        self.prev_output = output

        return output