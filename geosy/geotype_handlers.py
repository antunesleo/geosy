from shapely import wkt, geometry as shapely_geometry
from geomet import wkt as geomet_wkt
from geojson_rewind import rewind

from geosy.enums import GeoFormats, GeoShapes
from geosy.custom_typing import AnyShapelyGeoType, AnyGeoType, AnyWktGeoType, AnyGeoJsonGeoType
from geosy.exceptions import UnsupportedGeoTypeError, UnsupportedShapeError, UnsupportedError
from geosy.geotypes import Wkt, GeoJsonPolygon, WktPolygon

__all__ = [
    'ALL_SHAPELY_TYPES',
    'ALL_WKT_TYPES',
    'identify_geo_type',
    'is_geometry_valid',
    'create_geo_json',
    'create_wkt',
    'geometry_type_converter'
]

ALL_SHAPELY_TYPES = (
    shapely_geometry.Polygon
)

ALL_WKT_TYPES = (
    WktPolygon
)


def identify_geo_type(unknown_geo_type: AnyGeoType) -> GeoFormats:
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


def create_geo_json(geo_json: dict) -> AnyGeoJsonGeoType:
    shape = geo_json['type'].lower()

    if geo_json['type'].lower() == GeoShapes.POLYGON.value.lower():
        return GeoJsonPolygon(geo_json)

    error_message = f'could not create an geo json instance because the shape {shape} is not supported'
    raise UnsupportedShapeError(error_message)


def create_wkt(wkt: str) -> AnyWktGeoType:
    shape = wkt.split(' ')[0].lower()

    if shape == GeoShapes.POLYGON.value.lower():
        return WktPolygon(wkt)

    error_message = f'could not create an wkt instance because the shape {shape} is not supported'
    raise UnsupportedShapeError(error_message)


class GeometryTypeConverter:

    def from_unknown_to_spec_type(self, unknown_geometry: AnyGeoType, spec_type: GeoFormats):
        known_geometry_type = identify_geo_type(unknown_geometry)
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
