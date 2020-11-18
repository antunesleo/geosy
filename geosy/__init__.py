from enum import Enum
from typing import Union

from shapely import geometry as shapely_geometry

from geosy.geotypes import WktPolygon, GeoJsonPolygon

ALL_SHAPELY_TYPES = (
    shapely_geometry.MultiPoint,
    shapely_geometry.Point,
    shapely_geometry.Polygon,
    shapely_geometry.MultiPolygon,
    shapely_geometry.LineString,
    shapely_geometry.MultiLineString,
    shapely_geometry.LinearRing
)

AnyGeoType = Union[
    WktPolygon,
    GeoJsonPolygon,
    shapely_geometry.MultiPoint,
    shapely_geometry.Point,
    shapely_geometry.Polygon,
    shapely_geometry.MultiPolygon,
    shapely_geometry.LineString,
    shapely_geometry.MultiLineString,
    shapely_geometry.LinearRing
]

AnyShapelyGeoType = Union[
    shapely_geometry.MultiPoint,
    shapely_geometry.Point,
    shapely_geometry.Polygon,
    shapely_geometry.MultiPolygon,
    shapely_geometry.LineString,
    shapely_geometry.MultiLineString,
    shapely_geometry.LinearRing
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


class GeoFormats(Enum):
    WKT = 'wkt'
    SHAPELY = 'shapely'


class GeoShapes(Enum):
    MULTIPOINT = 'multipoint'
    POINT = 'point'
    POLYGON = 'polygon'
    MULTIPOLYGON = 'multipolygon'
    LINESTRING = 'linestring',
    MULTILINESTRING = 'multilinestring',
    LINEARRING = 'linearring'
