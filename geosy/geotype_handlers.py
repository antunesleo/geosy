from shapely import wkt
from geomet import wkt as geomet_wkt
from geojson_rewind import rewind

from geosy import GeoFormats, AnyShapelyGeoType, AnyGeoType, ALL_SHAPELY_TYPES
from geosy.exceptions import UnsupportedGeoTypeError
from geosy.geotypes import Wkt


class Identifier:

    def identify_geo_type(self, unknown_geo_type: AnyGeoType) -> GeoFormats:
        if isinstance(unknown_geo_type, ALL_SHAPELY_TYPES):
            return GeoFormats.SHAPELY

        if isinstance(unknown_geo_type, Wkt):
            return GeoFormats.WKT

        raise UnsupportedGeoTypeError(f'The type {unknown_geo_type} is not supported')


identifier = Identifier()


class GeometryTypeConverter:

    def __init__(self, geo_type_identifier: Identifier):
        self.__identifier = geo_type_identifier

    def from_unknown_to_spec_type(self, unknown_geometry: AnyGeoType, spec_type: GeoFormats):
        known_geometry_type = self.__identifier.identify_geo_type(unknown_geometry)
        method_name = f'from_{known_geometry_type.value}_to_{spec_type.value}'
        method_to_call = getattr(self, method_name)
        return method_to_call(unknown_geometry)

    @staticmethod
    def from_shapely_to_wkt(shapely_geometry: AnyShapelyGeoType) -> Wkt:
        return Wkt(shapely_geometry.wkt)

    @staticmethod
    def from_wkt_to_shapely(wkt_geometry: Wkt) -> AnyShapelyGeoType:
        return wkt.loads(wkt_geometry.as_str)

    def from_wkt_to_geojson(self, wkt_geometry: Wkt) -> dict:
        geojson = geomet_wkt.loads(wkt_geometry.as_str)
        return self.__fix_to_right_hand_rule(geojson)

    @staticmethod
    def __fix_to_right_hand_rule(geojson: dict) -> dict:
        """
        There are functions that return a GEOJSON in the wrong format, that is, it does not follow
        the "right hand" rule, which means that our coordinates follow a single direction
        this function is here to correct this problem.
        """
        return rewind(geojson)


class Validator:

    def is_geometry_valid(self, geometry: AnyGeoType) -> bool:
        pass


geometry_type_converter = GeometryTypeConverter(Identifier())
