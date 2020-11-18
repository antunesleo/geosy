from unittest import TestCase

from geosy.geotypes import Wkt
from geosy.exceptions import CorruptedGeometryError
from geosy.geotypes import GeoJsonPolygon

from tests.dataset import geojson as geojson_dataset, wkt as wkt_dataset


class TestWkt(TestCase):

    def test_init_should_raise_corrupted_geometry_when_geometry_is_corrupted(self):
        corrupted_wkt = wkt_dataset.POINT_CURRPTED_BY_COMMA_BETWEEN_COORDINATES
        with self.assertRaises(CorruptedGeometryError):
            Wkt(corrupted_wkt)

    def test_should_have_as_str(self):
        wkt = Wkt(wkt_dataset.POINT)
        self.assertEqual(wkt_dataset.POINT, wkt.as_str)
        self.assertEqual(wkt_dataset.POINT, str(wkt))

    def test_is_valid_should_return_True_when_is_valid(self):
        wkt = Wkt(wkt_dataset.POINT)
        self.assertTrue(wkt.is_valid)

    def test_is_valid_should_return_False_when_is_invalid(self):
        invalid_wkt = Wkt(wkt_dataset.POLYGON_INVALID_WITH_CROSS_VERTICES)
        self.assertFalse(invalid_wkt.is_valid)


# TODO: Implement these tests
class TestPolygonWkt(TestCase):
    pass


class TestPolygonGeoJson(TestCase):

    def test_is_valid_should_return_True_when_is_valid(self):
        polygon_geojson = GeoJsonPolygon(geojson_dataset.POLYGON)
        self.assertTrue(polygon_geojson.is_valid)

    def test_is_valid_should_return_False_when_is_invalid(self):
        polygon_geojson = GeoJsonPolygon(geojson_dataset.POLYGON_INVALID_WITH_ONE_MORE_COORDINATE)
        self.assertFalse(polygon_geojson.is_valid)

    def test_init_should_raise_corrupted_geometry_when_geometry_has_string_instead_of_number_in_coordinates(self):
        with self.assertRaises(CorruptedGeometryError):
            GeoJsonPolygon(geojson_dataset.POLYGON_CORRUPTED_WITH_STRING_INSTEAD_OF_NUMBER_IN_COORDINATES)

    def test_should_have_as_dict(self):
        polygon_geojson = GeoJsonPolygon(geojson_dataset.POLYGON)
        self.assertEqual(geojson_dataset.POLYGON, polygon_geojson.as_dict)
