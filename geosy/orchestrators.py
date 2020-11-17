from ctypes import Union

from geosy.geotype_handlers import geometry_type_converter


class Orchestrator:
    pass


class PolygonOrchestrator(Orchestrator):

    def merge_two_polygons(self, first_polygon: Union[Polygon, Wkt], second_polygon):
        pass
