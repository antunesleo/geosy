from shapely import wkt
from shapely.geometry.base import BaseGeometry
from geomet import wkt as geomet_wkt
from geojson_rewind import rewind

from geosy.geotypes import Wkt


class GeometryTypeConverter:

    def unknown_to(self, unknown_geometry: object, type_to_be_converted: str):
        pass

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

