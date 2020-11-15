from shapely import wkt
from shapely.geometry.base import BaseGeometry

from geosy.geotypes import Wkt


class GeometryConverter:

    def unknown_to(self, unknown_geometry: object, type_to_be_converted: str):
        pass

    def from_shapely_to_wkt(self, shapely_geometry: BaseGeometry) -> Wkt:
        return Wkt(shapely_geometry.wkt)

    def from_wkt_to_shapely(self, wkt_geometry: Wkt) -> BaseGeometry:
        return wkt.loads(wkt_geometry.as_str)
