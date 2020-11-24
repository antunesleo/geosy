from unittest import TestCase
from tests.datasets import wkt_str_dataset

from geosy import merge_polygons


class TestMergePolygons(TestCase):

    def test_should_merge_wkt_polygons(self):
        merged_wkt_polygon = merge_polygons((
            wkt_str_dataset.MERGEABLE_POLYGON_1,
            wkt_str_dataset.MERGEABLE_POLYGON_2
        ))

        self.assertEqual(merged_wkt_polygon, wkt_str_dataset.MERGED_POLYGON)
