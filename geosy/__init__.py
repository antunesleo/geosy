from geosy.geometries import AnyPolygonType, create_wkt, create_geo_json, ALL_SHAPELY_TYPES, create_geometry, \
    return_geometry
from  geosy.facades import polygon_facade

__all__ = ['merge_polygons']

ALL_INTERNAL_GEOMETRIES = []


def merge_polygons(polygons: tuple) -> AnyPolygonType:
    merged_polygon = polygon_facade.merge_polygons(polygons)
    return merged_polygon

