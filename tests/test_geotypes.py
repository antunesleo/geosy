from unittest import TestCase

from geosy.geotypes import Wkt
from geosy.exceptions import CorruptedGeometryError
from geosy.geotypes import GeoJsonPolygon
from tests.dataset import geojson


class TestWkt(TestCase):

    def test_init_should_raise_corrupted_geometry_when_geometry_is_corrupted(self):
        corrupted_wkt = 'POINT (40.12, 40.32)'
        with self.assertRaises(CorruptedGeometryError):
            Wkt(corrupted_wkt)

    def test_should_have_as_str(self):
        wkt = Wkt('POINT (40.12 40.32)')
        self.assertEqual('POINT (40.12 40.32)', wkt.as_str)
        self.assertEqual('POINT (40.12 40.32)', str(wkt))

    def test_is_valid_should_return_True_when_is_valid(self):
        wkt = Wkt('POINT (40.12 40.32)')
        self.assertTrue(wkt.is_valid)

    def test_is_valid_should_return_False_when_is_invalid(self):
        invalid_wkt = Wkt('POLYGON((-48.245889694525026 -22.858927941361873,-48.24623301727893 -22.875061322884815,-48.23112681610706 -22.85165147590018,-48.22082713348987 -22.873005214130387,-48.245889694525026 -22.858927941361873))')
        self.assertFalse(invalid_wkt.is_valid)


class TestPolygonGeoJson(TestCase):

    def test_is_valid_should_return_True_when_is_valid(self):
        polygon_geojson = GeoJsonPolygon(geojson.POLYGON)
        self.assertTrue(polygon_geojson.is_valid)

    def test_is_valid_should_return_False_when_is_invalid(self):
        polygon_geojson = GeoJsonPolygon(geojson.POLYGON_INVALID_WITH_ONE_MORE_COORDINATE)
        self.assertFalse(polygon_geojson.is_valid)

    def test_init_should_raise_corrupted_geometry_when_geometry_has_string_instead_of_number_in_coordinates(self):
        with self.assertRaises(CorruptedGeometryError):
            GeoJsonPolygon(geojson.POLYGON_CORRUPTED_WITH_STRING_INSTEAD_OF_NUMBER_IN_COORDINATES)

    def test_should_have_as_dict(self):
        polygon_geojson = GeoJsonPolygon(geojson.POLYGON)
        self.assertEqual(geojson.POLYGON, polygon_geojson.as_dict)
