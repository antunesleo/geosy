from typing import Union

from shapely import geometry as shapely_geometry

from geosy.geotypes import WktPolygon, GeoJsonPolygon


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