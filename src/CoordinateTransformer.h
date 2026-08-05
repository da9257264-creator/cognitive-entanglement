#ifndef COORDINATE_TRANSFORMER_H
#define COORDINATE_TRANSFORMER_H

namespace CognitiveEntanglement {

    struct GeodeticPoint {
        double latitude;  // in degrees
        double longitude; // in degrees
        double altitude;  // in meters
    };

    struct NedVector {
        double north;     // in meters
        double east;      // in meters
        double down;      // in meters
    };

    /// High-Performance Aerospace Coordinate Frame Transformer.
    /// Written in Modern C++ to perform sub-microsecond Geodetic (WGS84)
    /// to Local Tangent Plane (NED - North, East, Down) projections.
    class CoordinateTransformer {
    public:
        CoordinateTransformer(double ref_latitude, double ref_longitude, double ref_altitude);

        NedVector GeodeticToNed(const GeodeticPoint& target) const;

    private:
        double _ref_lat_rad;
        double _ref_lon_rad;
        double _ref_alt;

        // WGS84 Ellipsoid constants
        static constexpr double a = 6378137.0;          // semi-major axis (meters)
        static constexpr double f = 1.0 / 298.257223563; // flattening
        static constexpr double b = a * (1.0 - f);      // semi-minor axis
        static constexpr double e_sq = f * (2.0 - f);   // eccentricity squared

        struct EcefPoint {
            double x;
            double y;
            double z;
        };

        EcefPoint GeodeticToEcef(const GeodeticPoint& geo) const;
    };

}

#endif // COORDINATE_TRANSFORMER_H
