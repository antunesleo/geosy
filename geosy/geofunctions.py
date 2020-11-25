from typing import Tuple

from shapely import ops
from shapely.geometry import Polygon

from geosy.exceptions import SeparatedPolygonsError


def merge_polygons(polygons: Tuple[Polygon]) -> Polygon:
    merged_polygon = ops.cascaded_union(polygons)
    if not isinstance(merged_polygon, Polygon):
        raise SeparatedPolygonsError('Could not merge polygons because they are not touching')

    return merged_polygon
