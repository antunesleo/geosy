from unittest import TestCase

from geosy.tools import GeoFunctions
from tests.datasets import wkt_str_dataset

from geosy.facades import PolygonFacade
from geosy.tools import GeometryTypeConverter


class TestPolygonFacade(TestCase):

    def test_should_raise_ValueError_when_polygons_tuples_does_not_have_at_least_2_items(self):
        facade = PolygonFacade(GeometryTypeConverter(), GeoFunctions())

        with self.assertRaises(ValueError):
            facade.merge_polygons(tuple())

    def test_should_merge_two_wkt_polygons(self):
        facade = PolygonFacade(GeometryTypeConverter(), GeoFunctions())
        polygons = (wkt_str_dataset.MERGEABLE_POLYGON_1, wkt_str_dataset.MERGEABLE_POLYGON_2)

        merged_wkt_str_polygon = facade.merge_polygons(polygons)

        self.assertEqual(merged_wkt_str_polygon, wkt_str_dataset.MERGED_POLYGON)
