from unittest import TestCase

from geosy.geometries import Wkt, WktPolygon
from geosy.exceptions import CorruptedGeometryError
from geosy.geometries import GeoJsonPolygon

from tests.datasets import wkt_str_dataset as wkt_dataset
from tests.datasets import geojson_dict_dataset as geojson_dataset


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


class TestWktPolygon(TestCase):

    def test_init_should_raise_corrupted_geometry_when_geometry_is_corrupted(self):
        corrupted_wkt_polygon = wkt_dataset.POLYGON_CORRUPTED_BY_COMMA_BETWEEN_COORDINATES
        with self.assertRaises(CorruptedGeometryError):
            Wkt(corrupted_wkt_polygon)

    def test_should_have_as_str(self):
        wkt_polygon = WktPolygon(wkt_dataset.POLYGON)
        self.assertEqual(wkt_dataset.POLYGON, wkt_polygon.as_str)
        self.assertEqual(wkt_dataset.POLYGON, str(wkt_polygon))

    def test_is_valid_should_return_True_when_is_valid(self):
        wkt_polygon = WktPolygon(wkt_dataset.POLYGON)
        self.assertTrue(wkt_polygon.is_valid)

    def test_is_valid_should_return_False_when_is_invalid(self):
        invalid_wkt_polygon = WktPolygon(wkt_dataset.POLYGON_INVALID_WITH_CROSS_VERTICES)
        self.assertFalse(invalid_wkt_polygon.is_valid)

    def test_init_should_raise_value_error_when_shape_is_not_a_polygon(self):
        with self.assertRaises(ValueError):
            WktPolygon(wkt_dataset.POINT)


class TestGeoJsonPolygon(TestCase):

    def test_is_valid_should_return_True_when_is_valid(self):
        polygon_geojson = GeoJsonPolygon(geojson_dataset.POLYGON)
        self.assertTrue(polygon_geojson.is_valid)

    def test_is_valid_should_return_False_when_is_invalid(self):
        polygon_geojson = GeoJsonPolygon(geojson_dataset.POLYGON_INVALID_WITH_ONE_MORE_COORDINATE)
        self.assertFalse(polygon_geojson.is_valid)

    def test_init_should_raise_corrupted_geometry_when_geometry_has_string_instead_of_number_in_coordinates(self):
        with self.assertRaises(CorruptedGeometryError):
            GeoJsonPolygon(geojson_dataset.POLYGON_CORRUPTED_WITH_STRING_INSTEAD_OF_NUMBER_IN_COORDINATES)

    def test_init_should_raise_value_error_when_shape_is_not_a_polygon(self):
        with self.assertRaises(ValueError):
            GeoJsonPolygon(geojson_dataset.POINT)

    def test_should_have_as_dict(self):
        polygon_geojson = GeoJsonPolygon(geojson_dataset.POLYGON)
        self.assertEqual(geojson_dataset.POLYGON, polygon_geojson.as_dict)
