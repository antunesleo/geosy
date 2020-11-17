from typing import Union

from shapely import geometry as shapely_geometry

from geosy.exceptions import UnsupportedGeotypeError
from geosy import GeoFormats


class Wkt:

    def __init__(self, value_wkt: str):
        self.__value_wkt = value_wkt

    @property
    def as_str(self) -> str:
        return self.__value_wkt


class GeoTypeIdentifier:

    def identify_geotype(self, unknown_geotype) -> GeoFormats:
        if isinstance(
            unknown_geotype,
            (
                shapely_geometry.MultiPoint,
                shapely_geometry.Point,
                shapely_geometry.Polygon,
                shapely_geometry.MultiPolygon,
                shapely_geometry.LineString,
                shapely_geometry.MultiLineString,
                shapely_geometry.LinearRing)):
            return GeoFormats.SHAPELY

        if isinstance(unknown_geotype, Wkt):
            return GeoFormats.WKT

        raise UnsupportedGeotypeError(f'The type {unknown_geotype} is not supported')


identifier = GeoTypeIdentifier()
