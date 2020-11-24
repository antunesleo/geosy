from unittest import TestCase

from tests.datasets import wkt_str_dataset

from geosy.facades import PolygonFacade
from geosy.geotype_handlers import GeometryTypeConverter
from geosy.geotypes import WktPolygon


class TestPolygonFacade(TestCase):

    def test_should_raise_ValueError_when_polygons_tuples_does_not_have_at_least_2_items(self):
        facade = PolygonFacade(GeometryTypeConverter())

        with self.assertRaises(ValueError):
            facade.merge_polygons(tuple())

    def test_should_merge_two_wkt_polygons(self):
        facade = PolygonFacade(GeometryTypeConverter())
        polygons = (WktPolygon(wkt_str_dataset.MERGEABLE_POLYGON_1), WktPolygon(wkt_str_dataset.MERGEABLE_POLYGON_2))

        merged_wkt_polygon = facade.merge_polygons(polygons)

        self.assertIsInstance(merged_wkt_polygon, WktPolygon)
        self.assertEqual(merged_wkt_polygon.as_str, wkt_str_dataset.MERGED_POLYGON)
