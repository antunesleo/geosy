from typing import Union

from shapely import wkt
from shapely.geometry.base import BaseGeometry
from geomet import wkt as geomet_wkt
from geojson_rewind import rewind

from geosy import GeoFormats
from geosy.geotypes import identifier, Wkt, GeoTypeIdentifier


class GeometryTypeConverter:

    def __init__(self, geotype_identifier: GeoTypeIdentifier):
        self.__geotype_identifier = geotype_identifier

    def from_unknown_to_spec_type(self, unknown_geometry: object, spec_type: GeoFormats):
        known_geometry_type = self.__geotype_identifier.identify_geotype(unknown_geometry)
        method_name = f'from_{known_geometry_type.value}_to_{spec_type.value}'
        method_to_call = getattr(self, method_name)
        return method_to_call(unknown_geometry)

    def from_shapely_to_wkt(self, shapely_geometry: BaseGeometry) -> Wkt:
        return Wkt(shapely_geometry.wkt)

    def from_wkt_to_shapely(self, wkt_geometry: Wkt) -> BaseGeometry:
        return wkt.loads(wkt_geometry.as_str)

    def from_wkt_to_geojson(self, wkt_geometry: Wkt) -> dict:
        geojson = geomet_wkt.loads(wkt_geometry.as_str)
        return self.__fix_to_right_hand_rule(geojson)

    def __fix_to_right_hand_rule(self, geojson: dict) -> dict:
        """
        There are functions that return a GEOJSON in the wrong format, that is, it does not follow
        the "right hand" rule, which means that our coordinates follow a single direction
        this function is here to correct this problem.
        """
        return rewind(geojson)


geometry_type_converter = GeometryTypeConverter(identifier)
