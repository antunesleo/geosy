from shapely import wkt, geometry as shapely_geometry
from geomet import wkt as geomet_wkt
from geojson_rewind import rewind

from geosy.geometries import GeoFormats
from geosy.geometries import Wkt, AnyShapelyGeoType, AnyGeoType, AnyWktGeoType, AnyGeoJsonGeoType
from geosy.geometries import create_wkt, create_geo_json
from geosy.geometries import ALL_SHAPELY_TYPES, ALL_WKT_TYPES
from geosy.exceptions import UnsupportedGeoTypeError, UnsupportedError

__all__ = [
    'identify_geometry_type',
    'is_geometry_valid',
    'GeometryTypeConverter',
    'geometry_type_converter'
]


def identify_geometry_type(unknown_geo_type: AnyGeoType) -> GeoFormats:
    if isinstance(unknown_geo_type, ALL_SHAPELY_TYPES):
        return GeoFormats.SHAPELY

    if isinstance(unknown_geo_type, ALL_WKT_TYPES):
        return GeoFormats.WKT

    raise UnsupportedGeoTypeError(f'The type {unknown_geo_type} is not supported')


def is_geometry_valid(geometry: AnyGeoType) -> bool:
    if isinstance(geometry, AnyWktGeoType):
        return geometry.is_valid

    if isinstance(geometry, AnyGeoJsonGeoType):
        return geometry.is_valid

    raise UnsupportedError(f'cant validate because type {type(geometry)} is not supported')


class GeometryTypeConverter:

    def from_unknown_to_spec_type(self, unknown_geometry: AnyGeoType, spec_type: GeoFormats):
        known_geometry_type = identify_geometry_type(unknown_geometry)
        method_name = f'from_{known_geometry_type.value}_to_{spec_type.value}'
        method_to_call = getattr(self, method_name)
        return method_to_call(unknown_geometry)

    def from_shapely_to_wkt(self, shapely_geometry: AnyShapelyGeoType) -> AnyWktGeoType:
        return create_wkt(shapely_geometry.wkt)

    @staticmethod
    def from_wkt_to_shapely(wkt_geometry: Wkt) -> AnyShapelyGeoType:
        return wkt.loads(wkt_geometry.as_str)

    def from_wkt_to_geojson(self, wkt_geometry: Wkt) -> AnyGeoJsonGeoType:
        geojson = geomet_wkt.loads(wkt_geometry.as_str)
        return create_geo_json(self.__fix_to_right_hand_rule(geojson))

    @staticmethod
    def __fix_to_right_hand_rule(geojson: dict) -> dict:
        """
        There are functions that return a GEOJSON in the wrong format, that is, it does not follow
        the "right hand" rule, which means that our coordinates follow a single direction
        this function is here to correct this problem.
        """
        return rewind(geojson)


geometry_type_converter = GeometryTypeConverter()
