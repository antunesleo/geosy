from unittest import TestCase

from geosy.facades import PolygonFacade
from geosy.geotype_handlers import Validator, GeometryTypeConverter, Identifier, GeoTypesFactory
from geosy.geotypes import WktPolygon
from tests.datasets import wkt_dataset


class TestPolygonFacade(TestCase):

    def test_should_merge_two_polygons(self):
        facade = PolygonFacade(
            Validator(),
            GeometryTypeConverter(
                Identifier(),
                GeoTypesFactory()
            )
        )
        polygons = (WktPolygon(wkt_dataset.MERGEABLE_POLYGON_1), WktPolygon(wkt_dataset.MERGEABLE_POLYGON_2))
        merged_wkt_polygon = facade.merge_polygons(polygons)
        self.assertIsInstance(merged_wkt_polygon, WktPolygon)
        self.assertEqual(merged_wkt_polygon.as_str, wkt_dataset.MERGED_POLYGON)
