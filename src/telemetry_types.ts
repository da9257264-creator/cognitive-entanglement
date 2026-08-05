/**
 * Cognitive Entanglement - Unified Telemetry Interface Specifications.
 * Language: TypeScript (TS)
 * Purpose: Enforces compile-time type-safety, interface contracts, and 
 * strict packet schemas for our high-speed WebRTC/WebSocket communication channels.
 */

export interface Position3D {
    x: number; // local X coordinate (East-West displacement in meters)
    y: number; // local Y coordinate (North-South displacement in meters)
    z: number; // local Z coordinate (Altitude in meters)
}

export interface DroneTelemetryPacket {
    drone_id: number;
    connected: boolean;
    is_flying: boolean;
    position: Position3D;
    yaw: number;       // Heading rotation in degrees (0 - 360)
    battery: number;   // Simulated battery percentage (0 - 100)
    speed: number;     // Linear speed magnitude in meters/second
    flight_mode: "LANDED" | "HOVERING" | "GUIDED" | "NAVIGATING" | "SEC_LOCK" | "RETURNING" | "DRAW_FLY";
}

export interface ControlVectorsPacket {
    vx: number;    // Command forward velocity (pitch rate)
    vy: number;    // Command lateral velocity (roll rate)
    vz: number;    // Command vertical velocity (climb/descend rate)
    vyaw: number;  // Command rotational yaw velocity
}

export interface ClientTelemetryUpdate {
    gesture: "NONE" | "CROSS_HANDS" | "FIST" | "OPEN_PALM" | "ASL_ILY" | "ASL_PEACE" | "ASL_Y" | "ASL_THUMBS_UP" | "ASL_OK" | "ASL_WAIT";
    morse_cmd: string;
    voice_cmd: string;
    body_state: "MOVING" | "STOPPED";
    body_vectors: ControlVectorsPacket;
    face_landmarks: any | null; // MediaPipe High-dimensional facial coordinates array
    voice_speed_scale: number;  // Spoken scale modifier (0.5 to 1.8)
    voice_height_offset: number; // Spoken height adjustments (+/- 0.5m)
    draw_coords?: Position3D[]; // Drawing waypoint queue (Draw-To-Fly)
    formation_cmd?: "V-SHAPE" | "LINE" | "ORBIT";
    tracking_target_cmd?: string;
}
