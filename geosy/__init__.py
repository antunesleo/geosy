from geosy.geometries import create_wkt, create_geo_json, create_geometry, return_geometry
from geosy.geometries import ALL_SHAPELY_TYPES, AnyReturnablePolygon
from geosy.facades import polygon_facade

__all__ = ['merge_polygons']


def merge_polygons(polygons: tuple) -> AnyReturnablePolygon:
    merged_polygon = polygon_facade.merge_polygons(polygons)
    return merged_polygon
