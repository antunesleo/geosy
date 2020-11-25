from typing import Tuple

from shapely import ops, geometry as shapely_geometry

from geosy.geometries import GeoFormats, create_geometry, return_geometry, AnyReturnablePolygon
from geosy.exceptions import SeparatedPolygonsError
from geosy.tools import GeometryTypeConverter, identify_geometry_type, geometry_type_converter

__all__ = [
    'polygon_facade',
    'PolygonFacade'
]


class Facade:
    pass


class PolygonFacade(Facade):

    def __init__(self, converter: GeometryTypeConverter):
        self.__converter = converter

    def merge_polygons(self, polygons_data: Tuple) -> AnyReturnablePolygon:
        if len(polygons_data) < 2:
            raise ValueError(f'You must provide at least two polygons to be merge, {len(polygons_data)} provided.')

        polygons = tuple(create_geometry(polygon) for polygon in polygons_data)
        shapely_polygons = self.__convert_polygons_to_shapely(polygons)

        shapely_merged_polygon = ops.cascaded_union(shapely_polygons)
        if not isinstance(shapely_merged_polygon, shapely_geometry.Polygon):
            raise SeparatedPolygonsError('Could not merge polygons because they are not touching')

        geometry_type = identify_geometry_type(polygons[0])
        merged_polygon = self.__converter.from_unknown_to_spec_type(shapely_merged_polygon, spec_type=geometry_type)

        return return_geometry(merged_polygon)

    def __convert_polygons_to_shapely(self, polygons):
        shapely_polygons = []
        for polygon in polygons:
            shapely_polygons.append(self.__converter.from_unknown_to_spec_type(
                polygon,
                spec_type=GeoFormats.SHAPELY
            ))
        return shapely_polygons


polygon_facade = PolygonFacade(geometry_type_converter)
