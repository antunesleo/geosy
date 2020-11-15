from unittest import TestCase

from shapely.geometry import Polygon

from geosy.converters import GeometryConverter
from geosy.geotypes import Wkt


class TestGeometryConverter(TestCase):

    def test_should_convert_polygon_geometry_from_shapely_to_wkt(self):
        shapely_polygon = Polygon([
            [-50.1715041, -21.7928566],
            [-50.1744239, -21.7924781],
            [-50.1773223, -21.7929562],
            [-50.1784601, -21.7950084],
            [-50.1723414, -21.7959647],
            [-50.1715041, -21.7928566]
        ])
        converter = GeometryConverter()
        wkt_polygon = converter.from_shapely_to_wkt(shapely_polygon)
        self.assertIsInstance(wkt_polygon, Wkt)
        self.assertEqual(
            'POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))',
            wkt_polygon.as_str
        )

    def test_should_convert_polygon_geometry_from_wkt_to_shapely(self):
        wkt_polygon = Wkt('POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))')
        converter = GeometryConverter()
        shapely_polygon = converter.from_wkt_to_shapely(wkt_polygon)
        self.assertIsInstance(shapely_polygon, Polygon)
        self.assertEqual(
            'POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))',
            shapely_polygon.wkt
        )
