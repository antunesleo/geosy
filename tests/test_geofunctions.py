from unittest import TestCase

from geosy.geofunctions import merge_polygons
from tests.datasets import shapely_dataset


class TestMergePolygons(TestCase):

    def test_should_merge_two_wkt_polygons(self):
        polygons = (shapely_dataset.MERGEABLE_POLYGON_1, shapely_dataset.MERGEABLE_POLYGON_2)
        merged_polygon = merge_polygons(polygons)
        self.assertEqual(merged_polygon.wkt, shapely_dataset.MERGED_POLYGON.wkt)
