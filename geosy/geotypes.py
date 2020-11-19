from abc import ABC

import geojson as geojson_lib

from shapely import wkt
from shapely.errors import WKTReadingError

from geosy import GeoShapes
from geosy.exceptions import CorruptedGeometryError


class Wkt(ABC):

    def __init__(self, value_wkt: str):
        self.__wkt = value_wkt

        try:
            shapely_geometry = wkt.loads(self.__wkt)
        except WKTReadingError:
            raise CorruptedGeometryError(f'The wkt geometry {self.__wkt} is corrupted')

        self.__is_valid = shapely_geometry.is_valid

    def __str__(self):
        return self.__wkt

    @property
    def shape(self) -> str:
        return self.__wkt.split(' ')[0]

    @property
    def as_str(self) -> str:
        return self.__wkt

    @property
    def is_valid(self) -> bool:
        return self.__is_valid


class WktPolygon(Wkt):

    def __init__(self, value_wkt: str):
        super(WktPolygon, self).__init__(value_wkt)
        if self.shape.lower() != GeoShapes.POLYGON.value.lower():
            raise ValueError(f'A {self.shape} shape was provided for wkt polygon creation instead of a polygon shape')


class GeoJson:

    def __init__(self, geojson: dict):
        self._geojson = geojson

    @property
    def shape(self) -> str:
        return self._geojson['type']

    @property
    def as_dict(self) -> dict:
        return self._geojson


class GeoJsonPolygon(GeoJson):

    def __init__(self, geojson: dict):
        super(GeoJsonPolygon, self).__init__(geojson)

        try:
            geojson_lib_polygon = geojson_lib.Polygon(self._geojson['coordinates'])
            self.__is_valid = geojson_lib_polygon.is_valid
        except ValueError:
            raise CorruptedGeometryError(f'The geojson polygon {self._geojson} is corrupted')

        if self.shape.lower() != GeoShapes.POLYGON.value.lower():
            raise ValueError(f'A {self.shape} shape was provided for geo json polygon creation instead of a polygon shape')

    @property
    def as_dict(self) -> dict:
        return self._geojson

    @property
    def is_valid(self) -> bool:
        return self.__is_valid
