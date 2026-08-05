// ==============================================================================
// Cognitive Entanglement - ARM NEON SIMD Vector Math Optimization Library 📐⚙️
// Language: ARM Assembly (AArch64 / ASM)
// Target: ARMv8-A Cortex processors (Phone A / Raspberry Pi Onboard Companion)
// Purpose: Performs high-speed 4-lane parallel Single Instruction Multiple Data
//          (SIMD) float vector multiplications for real-time 3D flight coordinate
//          projections with zero latency.
// ==============================================================================

.text
.align 4
.global neon_vector_multiply
.type neon_vector_multiply, %function

// Function signature in C++:
// extern "C" void neon_vector_multiply(const float* a, const float* b, float* result, int length);
//
// Arguments passed in ARM64 registers:
// x0: Pointer to float array A (Input 1)
// x1: Pointer to float array B (Input 2)
// x2: Pointer to float array result (Output)
// w3: Integer length of arrays (must be multiple of 4)

neon_vector_multiply:
    // Check if length is zero
    cmp w3, #0
    ble .done

.loop:
    // Load 4 floats (128-bit) from array A into NEON register v0 (4S = 4 single precision floats)
    ld1 {v0.4s}, [x0], #16
    
    // Load 4 floats (128-bit) from array B into NEON register v1
    ld1 {v1.4s}, [x1], #16
    
    // Perform parallel 4-lane multiply: v2.4s = v0.4s * v1.4s (instantaneous float vector product)
    fmul v2.4s, v0.4s, v1.4s
    
    // Store 4 result floats from NEON register v2 into result array
    st1 {v2.4s}, [x2], #16
    
    // Subtract 4 from length loop counter
    sub w3, w3, #4
    
    // Compare loop counter to zero
    cmp w3, #0
    bgt .loop

.done:
    ret
