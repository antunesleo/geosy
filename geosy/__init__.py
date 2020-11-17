from enum import Enum
from typing import Union

from shapely import geometry as shapely_geometry

from geosy.geotypes import Wkt


ALL_SHAPELY_TYPES = (
    shapely_geometry.MultiPoint,
    shapely_geometry.Point,
    shapely_geometry.Polygon,
    shapely_geometry.MultiPolygon,
    shapely_geometry.LineString,
    shapely_geometry.MultiLineString,
    shapely_geometry.LinearRing
)

AnyShapelyGeoType = Union[
    shapely_geometry.MultiPoint,
    shapely_geometry.Point,
    shapely_geometry.Polygon,
    shapely_geometry.MultiPolygon,
    shapely_geometry.LineString,
    shapely_geometry.MultiLineString,
    shapely_geometry.LinearRing
]


AnyGeoType = Union[
    Wkt,
    dict,
    shapely_geometry.MultiPoint,
    shapely_geometry.Point,
    shapely_geometry.Polygon,
    shapely_geometry.MultiPolygon,
    shapely_geometry.LineString,
    shapely_geometry.MultiLineString,
    shapely_geometry.LinearRing
]


class GeoFormats(Enum):
    WKT = 'wkt'
    SHAPELY = 'shapely'
