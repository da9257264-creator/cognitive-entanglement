-- ==============================================================================
-- Cognitive Entanglement - Functional Infinite Impulse Response (IIR) DSP Filter
-- Language: Haskell (GHC Specification)
-- Target: High-Integrity Ground Station Signal Processing & Calibration
-- Purpose: Implements a clean, stateless First-Order High-Pass IIR Filter
--          to remove low-frequency sensor drift (IMU bias) from accelerometer feeds.
-- ==============================================================================

module SensorFilter (
    highPassFilter
) where

-- | First-Order High-Pass IIR Filter Equation:
--   y[n] = alpha * (y[n-1] + x[n] - x[n-1])
--   
--   Arguments:
--   alpha : Filter cutoff scaling factor (0.0 to 1.0)
--   prevX : Previous input value (x[n-1])
--   prevY : Previous output value (y[n-1])
--   currX : Current input value (x[n])
highPassFilterStep :: Double -> Double -> Double -> Double -> Double
highPassFilterStep alpha prevX prevY currX = alpha * (prevY + currX - prevX)

-- | Recursively filters an entire list of noisy sensor readings using a stateless fold.
--   Returns a clean list of high-pass filtered values.
highPassFilter :: Double -> [Double] -> [Double]
highPassFilter alpha signals = reverse (foldl step [] signals)
  where
    step [] x = [x] -- Initial state: first output is equal to first input
    step acc@(prevY:_) currX =
      let prevX = head (drop (length acc - 1) acc) -- Approximate x[n-1]
          newY = highPassFilterStep alpha prevX prevY currX
      in newY : acc

main :: IO ()
main = do
    putStrLn "COGNITIVE ENTANGLEMENT: Haskell DSP Sensor Filter Initialized."
    let noisySignals = [1.0, 1.1, 1.2, 5.0, 4.8, 1.1, 1.0] -- Simulated sensor spike
    let filtered = highPassFilter 0.85 noisySignals
    putStrLn $ "Noisy input signal: " ++ show noisySignals
    putStrLn $ "Filtered output signal: " ++ show filtered
