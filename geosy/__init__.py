from enum import Enum
from typing import Union

from shapely import geometry as shapely_geometry

from geosy.geotypes import WktPolygon, GeoJsonPolygon

ALL_SHAPELY_TYPES = (
    shapely_geometry.Polygon
)

ALL_WKT_TYPES = (
    WktPolygon
)

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
