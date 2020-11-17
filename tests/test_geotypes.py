from unittest import TestCase, mock

from shapely.geometry import Polygon

from geosy import GeoFormats, exceptions
from geosy.geotypes import GeoTypeIdentifier


class TestGeoTypeIdentifier(TestCase):

    def test_should_identify_shapely_geo_type(self):
        shapely_polygon = Polygon([
            [-50.1715041, -21.7928566],
            [-50.1744239, -21.7924781],
            [-50.1773223, -21.7929562],
            [-50.1784601, -21.7950084],
            [-50.1723414, -21.7959647],
            [-50.1715041, -21.7928566]
        ])
        identifier = GeoTypeIdentifier()
        geotype = identifier.identify_geotype(shapely_polygon)
        self.assertEqual(GeoFormats.SHAPELY, geotype)

    def test_identify_should_raise_unsupported_geotype(self):
        unsupported_type = mock.MagicMock()
        identifier = GeoTypeIdentifier()
        with self.assertRaises(exceptions.UnsupportedGeotypeError):
            identifier.identify_geotype(unsupported_type)
