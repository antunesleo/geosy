from unittest import TestCase

from shapely.geometry import Polygon

from geosy.converters import GeometryTypeConverter
from geosy.geotypes import Wkt


class TestGeometryTypeConverter(TestCase):

    def test_should_convert_polygon_geometry_from_shapely_to_wkt(self):
        shapely_polygon = Polygon([
            [-50.1715041, -21.7928566],
            [-50.1744239, -21.7924781],
            [-50.1773223, -21.7929562],
            [-50.1784601, -21.7950084],
            [-50.1723414, -21.7959647],
            [-50.1715041, -21.7928566]
        ])
        converter = GeometryTypeConverter()
        wkt_polygon = converter.from_shapely_to_wkt(shapely_polygon)
        self.assertIsInstance(wkt_polygon, Wkt)
        self.assertEqual(
            'POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))',
            wkt_polygon.as_str
        )

    def test_should_convert_polygon_geometry_from_wkt_to_shapely(self):
        wkt_polygon = Wkt('POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))')
        converter = GeometryTypeConverter()
        shapely_polygon = converter.from_wkt_to_shapely(wkt_polygon)
        self.assertIsInstance(shapely_polygon, Polygon)
        self.assertEqual(
            'POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))',
            shapely_polygon.wkt
        )

    def test_should_convert_polygon_geometry_from_wkt_to_geojson_polygon(self):
        wkt_polygon = Wkt('POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))')
        converter = GeometryTypeConverter()
        geojson_polygon = converter.from_wkt_to_geojson(wkt_polygon)
        print(geojson_polygon)
        self.assertIsInstance(geojson_polygon, dict)
        self.assertEqual({'type': 'Polygon', 'coordinates': [[[-50.1715041, -21.7928566], [-50.1744239, -21.7924781], [-50.1773223, -21.7929562], [-50.1784601, -21.7950084], [-50.1723414, -21.7959647], [-50.1715041, -21.7928566]]]}, geojson_polygon)
