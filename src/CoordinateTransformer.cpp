#include "CoordinateTransformer.h"
#include <cmath>

namespace CognitiveEntanglement {

    CoordinateTransformer::CoordinateTransformer(double ref_latitude, double ref_longitude, double ref_altitude)
        : _ref_alt(ref_altitude) {
        // Convert reference degrees to radians
        _ref_lat_rad = ref_latitude * M_PI / 180.0;
        _ref_lon_rad = ref_longitude * M_PI / 180.0;
    }

    CoordinateTransformer::EcefPoint CoordinateTransformer::GeodeticToEcef(const GeodeticPoint& geo) const {
        double lat_rad = geo.latitude * M_PI / 180.0;
        double lon_rad = geo.longitude * M_PI / 180.0;

        double N = a / std::sqrt(1.0 - e_sq * std::sin(lat_rad) * std::sin(lat_rad));

        EcefPoint ecef;
        ecef.x = (N + geo.altitude) * std::cos(lat_rad) * std::cos(lon_rad);
        ecef.y = (N + geo.altitude) * std::cos(lat_rad) * std::sin(lon_rad);
        ecef.z = (N * (1.0 - e_sq) + geo.altitude) * std::sin(lat_rad);

        return ecef;
    }

    NedVector CoordinateTransformer::GeodeticToNed(const GeodeticPoint& target) const {
        // Step 1: Convert reference point and target point to Earth-Centered, Earth-Fixed (ECEF) coordinates
        GeodeticPoint ref_geo = { _ref_lat_rad * 180.0 / M_PI, _ref_lon_rad * 180.0 / M_PI, _ref_alt };
        EcefPoint ref_ecef = GeodeticToEcef(ref_geo);
        EcefPoint target_ecef = GeodeticToEcef(target);

        // Calculate delta vector in ECEF frame
        double dx = target_ecef.x - ref_ecef.x;
        double dy = target_ecef.y - ref_ecef.y;
        double dz = target_ecef.z - ref_ecef.z;

        // Step 2: Rotate ECEF delta vector to Local Tangent Plane (NED)
        double sin_lat = std::sin(_ref_lat_rad);
        double cos_lat = std::cos(_ref_lat_rad);
        double sin_lon = std::sin(_ref_lon_rad);
        double cos_lon = std::cos(_ref_lon_rad);

        NedVector ned;
        ned.north = -sin_lat * cos_lon * dx - sin_lat * sin_lon * dy + cos_lat * dz;
        ned.east = -sin_lon * dx + cos_lon * dy;
        ned.down = -cos_lat * cos_lon * dx - cos_lat * sin_lon * dy - sin_lat * dz;

        return ned;
    }

}
