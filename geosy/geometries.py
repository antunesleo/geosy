from abc import ABC, abstractmethod
from typing import Union
from enum import Enum

import geojson as geojson_lib

from shapely import geometry as shapely_geometry
from shapely import wkt
from shapely.errors import WKTReadingError

from geosy.exceptions import CorruptedGeometryError, UnsupportedShapeError

__all__ = [
    'GeoFormats',
    'GeoShapes',
    'GeoJson',
    'Wkt',
    'create_wkt',
    'create_geo_json',
    'AnyGeoType',
    'AnyWktGeoType',
    'AnyPolygonType',
    'AnyShapelyGeoType',
    'AnyGeoJsonGeoType',
    'ALL_WKT_TYPES',
    'ALL_SHAPELY_TYPES'
]


class GeoFormats(Enum):
    WKT = 'wkt'
    SHAPELY = 'shapely'
    GEOJSON = 'geojson'


class GeoShapes(Enum):
    MULTIPOINT = 'multipoint'
    POINT = 'point'
    POLYGON = 'polygon'
    MULTIPOLYGON = 'multipolygon'
    LINESTRING = 'linestring',
    MULTILINESTRING = 'multilinestring',
    LINEARRING = 'linearring'


class Geometry(ABC):

    @property
    @abstractmethod
    def primitive_repr(self):
        pass


class Wkt(Geometry):

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
    def primitive_repr(self):
        return self.__wkt

    @property
    def is_valid(self) -> bool:
        return self.__is_valid


class WktPolygon(Wkt):

    def __init__(self, value_wkt: str):
        super(WktPolygon, self).__init__(value_wkt)
        if self.shape.lower() != GeoShapes.POLYGON.value.lower():
            raise ValueError(f'A {self.shape} shape was provided for wkt polygon creation instead of a polygon shape')


class GeoJson(Geometry):

    def __init__(self, geojson: dict):
        self._geojson = geojson

    @property
    def shape(self) -> str:
        return self._geojson['type']

    @property
    def as_dict(self) -> dict:
        return self._geojson

    @property
    def primitive_repr(self):
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


AnyGeoType = Union[
    WktPolygon,
    GeoJsonPolygon,
    shapely_geometry.Polygon
]

AnyShapelyGeoType = Union[
    shapely_geometry.Polygon
]

AnyGeoJsonGeoType = Union[
    GeoJsonPolygon
]

AnyPolygonType = Union[
    WktPolygon,
    shapely_geometry.Polygon,
    GeoJsonPolygon
]

AnyWktGeoType = Union[
    WktPolygon
]

ALL_SHAPELY_TYPES = (
    shapely_geometry.Polygon,
)

ALL_GDAL_TYPES = tuple()

ALL_GEOJSON_TYPES = (
    GeoJsonPolygon,
)

ALL_WKT_TYPES = (
    WktPolygon,
)

ALL_INTERNAL_TYPES = ALL_WKT_TYPES + ALL_GEOJSON_TYPES
ALL_EXTERNAL_TYPES = ALL_SHAPELY_TYPES + ALL_GDAL_TYPES


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


def create_geometry(geometry: object):
    if isinstance(geometry, str):
        return create_wkt(geometry)
    if isinstance(geometry, dict):
        return create_geo_json(geometry)

    return geometry


def return_geometry(geometry):
    if isinstance(geometry, ALL_INTERNAL_TYPES):
        return geometry.primitive_repr

    return geometry
