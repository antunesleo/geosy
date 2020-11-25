from unittest import TestCase

from geosy.geometries import create_geo_json
from tests.datasets import wkt_str_dataset
from tests.datasets import geojson_dict_dataset

from geosy import merge_polygons


class TestMergePolygons(TestCase):

    def test_should_merge_wkt_polygons(self):
        merged_wkt_polygon = merge_polygons((
            wkt_str_dataset.MERGEABLE_POLYGON_1,
            wkt_str_dataset.MERGEABLE_POLYGON_2
        ))
        self.assertEqual(merged_wkt_polygon, wkt_str_dataset.MERGED_POLYGON)

    def test_should_merge_geojson_polygons(self):
        merged_wkt_polygon = merge_polygons((
            create_geo_json(geojson_dict_dataset.MERGEABLE_POLYGON_1),
            create_geo_json(geojson_dict_dataset.MERGEABLE_POLYGON_2)
        ))
        self.assertEqual(merged_wkt_polygon, geojson_dict_dataset.MERGED_POLYGON)

    def test_should_merge_shapely_polygons(self):
        pass
