from unittest import TestCase, mock

from shapely.geometry import Polygon

from geosy import GeoFormats
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
        converter = GeometryTypeConverter(mock.MagicMock())
        wkt_polygon = converter.from_shapely_to_wkt(shapely_polygon)
        self.assertIsInstance(wkt_polygon, Wkt)
        self.assertEqual(
            'POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))',
            wkt_polygon.as_str
        )

    def test_should_convert_polygon_geometry_from_wkt_to_shapely(self):
        wkt_polygon = Wkt('POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))')
        converter = GeometryTypeConverter(mock.MagicMock())
        shapely_polygon = converter.from_wkt_to_shapely(wkt_polygon)
        self.assertIsInstance(shapely_polygon, Polygon)
        self.assertEqual(
            'POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))',
            shapely_polygon.wkt
        )

    def test_should_convert_polygon_geometry_from_wkt_to_geojson_polygon(self):
        wkt_polygon = Wkt('POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))')
        converter = GeometryTypeConverter(mock.MagicMock())
        geojson_polygon = converter.from_wkt_to_geojson(wkt_polygon)
        self.assertIsInstance(geojson_polygon, dict)
        self.assertEqual({'type': 'Polygon', 'coordinates': [[[-50.1715041, -21.7928566], [-50.1744239, -21.7924781], [-50.1773223, -21.7929562], [-50.1784601, -21.7950084], [-50.1723414, -21.7959647], [-50.1715041, -21.7928566]]]}, geojson_polygon)

    def test_should_convert_from_unkown_to_spec_type(self):
        identifier_mock = mock.MagicMock()
        identifier_mock.identify_geotype.return_value = GeoFormats.WKT
        wkt_polygon = Wkt('POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))')
        converter = GeometryTypeConverter(identifier_mock)
        shapely_polygon = converter.from_unknown_to_spec_type(wkt_polygon, spec_type=GeoFormats.SHAPELY)
        self.assertIsInstance(shapely_polygon, Polygon)
        self.assertEqual(
            'POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))',
            shapely_polygon.wkt
        )

    def test_convert_from_unkown_to_spec_type_should_raise_exception_when_unkown_type_is_not_valid(self):
        pass

    def test_convert_from_unkown_to_spec_type_should_raise_exception_when_spec_type_is_not_valid(self):
        pass
