-- ==============================================================================
-- Cognitive Entanglement - Safety-Critical Altitude Boundary Limiter
-- Language: Ada (Ada 2012 Specification)
-- Target: High-Integrity Aerospace Systems (DO-178C Level A standard)
-- Purpose: Enforces strict, zero-runtime-exception flight boundaries.
-- ==============================================================================

package Altitude_Limiter is
   pragma Spark_Mode (On);

   type Altitude_Type is new Float range -100.0 .. 10000.0;
   type Velocity_Type is new Float range -50.0 .. 50.0;

   -- Clamps the vertical rate (velocity) based on safety geofence ceilings
   procedure Evaluate_Altitude_Limit (
      Current_Alt   : in     Altitude_Type;
      Max_Alt_Limit : in     Altitude_Type;
      Target_Rate   : in out Velocity_Type
   ) with
     Pre  => Max_Alt_Limit > 0.0,
     Post => (if Current_Alt >= Max_Alt_Limit then Target_Rate <= 0.0);

end Altitude_Limiter;
