from unittest import TestCase, mock

from shapely.geometry import Polygon

from tests.dataset import wkt as wkt_dataset

from geosy import GeoFormats
from geosy.geotype_handlers import GeometryTypeConverter, Identifier, GeoTypesFactory
from geosy.geotypes import Wkt, GeoJson, WktPolygon
from geosy.exceptions import UnsupportedGeoTypeError, UnsupportedShapeError


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
        geojson = converter.from_wkt_to_geojson(wkt_polygon)
        self.assertIsInstance(geojson, GeoJson)
        self.assertEqual({'type': 'Polygon', 'coordinates': [[[-50.1715041, -21.7928566], [-50.1744239, -21.7924781], [-50.1773223, -21.7929562], [-50.1784601, -21.7950084], [-50.1723414, -21.7959647], [-50.1715041, -21.7928566]]]}, geojson.as_dict)

    def test_should_convert_from_unknown_to_spec_type(self):
        identifier_mock = mock.MagicMock()
        identifier_mock.identify_geo_type.return_value = GeoFormats.WKT
        wkt_polygon = Wkt('POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))')
        converter = GeometryTypeConverter(identifier_mock)
        shapely_polygon = converter.from_unknown_to_spec_type(wkt_polygon, spec_type=GeoFormats.SHAPELY)
        self.assertIsInstance(shapely_polygon, Polygon)
        self.assertEqual(
            'POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))',
            shapely_polygon.wkt
        )

    def test_convert_from_unknown_to_spec_type_should_raise_exception_when_unknown_type_is_not_valid(self):
        identifier_mock = mock.MagicMock()
        identifier_mock.identify_geo_type.side_effect = UnsupportedGeoTypeError
        unknown_type = mock.MagicMock()

        with self.assertRaises(UnsupportedGeoTypeError):
            converter = GeometryTypeConverter(identifier_mock)
            converter.from_unknown_to_spec_type(unknown_type, spec_type=GeoFormats.SHAPELY)

    def test_convert_from_unknown_to_spec_type_should_raise_exception_when_spec_type_is_not_valid(self):
        wkt_polygon = WktPolygon('POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))')
        identifier_mock = mock.MagicMock()
        identifier_mock.identify_geo_type.side_effect = UnsupportedGeoTypeError

        with self.assertRaises(UnsupportedGeoTypeError):
            converter = GeometryTypeConverter(identifier_mock)
            converter.from_unknown_to_spec_type(wkt_polygon, spec_type='unsupported')


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
        identifier = Identifier()
        geotype = identifier.identify_geo_type(shapely_polygon)
        self.assertEqual(GeoFormats.SHAPELY, geotype)

    def test_should_identify_wkt_geo_type(self):
        wkt_polygon = WktPolygon('POLYGON ((-50.1715041 -21.7928566, -50.1744239 -21.7924781, -50.1773223 -21.7929562, -50.1784601 -21.7950084, -50.1723414 -21.7959647, -50.1715041 -21.7928566))')
        identifier = Identifier()
        geotype = identifier.identify_geo_type(wkt_polygon)
        self.assertEqual(GeoFormats.WKT, geotype)

    def test_identify_should_raise_unsupported_geotype(self):
        unsupported_type = mock.MagicMock()
        identifier = Identifier()
        with self.assertRaises(UnsupportedGeoTypeError):
            identifier.identify_geo_type(unsupported_type)


class TestGeoTypesFactory(TestCase):

    def test_should_create_wkt_polygon(self):
        factory = GeoTypesFactory()
        polygon_wkt = factory.create_wkt(wkt_dataset.POLYGON)
        self.assertIsInstance(polygon_wkt, WktPolygon)
        self.assertEqual(wkt_dataset.POLYGON, polygon_wkt.as_str)

    def test_should_raise_UnsupportedShapeError_when_shape_is_not_supported(self):
        factory = GeoTypesFactory()
        with self.assertRaises(UnsupportedShapeError):
            factory.create_wkt(wkt_dataset.POINT)
