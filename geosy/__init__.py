from enum import Enum


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
