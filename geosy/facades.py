from typing import Tuple

from shapely import ops, geometry as shapely_geometry

from geosy.enums import GeoFormats
from geosy.custom_typing import AnyPolygonType
from geosy.exceptions import SeparatedPolygonsError
from geosy.geotype_handlers import GeometryTypeConverter, identify_geo_type


class Facade:
    pass


class PolygonFacade(Facade):

    def __init__(self, converter: GeometryTypeConverter):
        self.__converter = converter

    def merge_polygons(self, polygons: Tuple):
        if len(polygons) < 2:
            raise ValueError(f'You must provide at least two polygons to be merge, {len(polygons)} provided.')

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

        return self.__converter.from_unknown_to_spec_type(shapely_merged_polygon, spec_type=input_type)
