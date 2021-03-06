from typing import Tuple

from geosy.geometries import GeoFormats, create_geometry, return_geometry, AnyReturnablePolygon
from geosy.tools import GeometryTypeConverter, GeoFunctions
from geosy.tools import geo_functions, identify_geometry_type, geometry_type_converter


__all__ = [
    'polygon_facade'
]


class Facade:
    pass


class PolygonFacade(Facade):

    def __init__(self, converter: GeometryTypeConverter, geo_functions: GeoFunctions):
        self.__converter = converter
        self.__geo_functions = geo_functions

    def merge_polygons(self, polygons_data: Tuple) -> AnyReturnablePolygon:
        if len(polygons_data) < 2:
            raise ValueError(f'You must provide at least two polygons to be merge, {len(polygons_data)} provided.')

        polygons = tuple(create_geometry(polygon) for polygon in polygons_data)
        shapely_polygons = self.__convert_polygons_to_shapely(polygons)

        shapely_merged_polygon = self.__geo_functions.merge_polygons(shapely_polygons)

        geometry_type = identify_geometry_type(polygons[0])
        merged_polygon = self.__converter.from_unknown_to_spec_type(shapely_merged_polygon, spec_type=geometry_type)

        return return_geometry(merged_polygon)

    def __convert_polygons_to_shapely(self, polygons) -> Tuple:
        shapely_polygons = []
        for polygon in polygons:
            shapely_polygons.append(self.__converter.from_unknown_to_spec_type(
                polygon,
                spec_type=GeoFormats.SHAPELY
            ))
        return tuple(shapely_polygons)


polygon_facade = PolygonFacade(geometry_type_converter, geo_functions)
