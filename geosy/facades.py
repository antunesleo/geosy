from typing import Tuple

from shapely import ops, geometry as shapely_geometry

from geosy.geometries import GeoFormats, create_geometry, return_geometry, AnyReturnablePolygon
from geosy.exceptions import SeparatedPolygonsError
from geosy.tools import GeometryTypeConverter, identify_geo_type, geometry_type_converter

__all__ = [
    'polygon_facade'
]


class Facade:
    pass


class PolygonFacade(Facade):

    def __init__(self, converter: GeometryTypeConverter):
        self.__converter = converter

    def merge_polygons(self, polygons: Tuple) -> AnyReturnablePolygon:
        if len(polygons) < 2:
            raise ValueError(f'You must provide at least two polygons to be merge, {len(polygons)} provided.')

        polygons = tuple(create_geometry(polygon) for polygon in polygons)

        input_type = identify_geo_type(polygons[0])

        shapely_polygons = [
            self.__converter.from_unknown_to_spec_type(
                polygon,
                spec_type=GeoFormats.SHAPELY
            )
            for polygon in polygons
        ]
        shapely_merged_polygon = ops.cascaded_union(shapely_polygons)
        if not isinstance(shapely_merged_polygon, shapely_geometry.Polygon):
            raise SeparatedPolygonsError('Could not merge polygons because they are not touching')

        merged_polygon = self.__converter.from_unknown_to_spec_type(shapely_merged_polygon, spec_type=input_type)
        return return_geometry(merged_polygon)


polygon_facade = PolygonFacade(geometry_type_converter)
