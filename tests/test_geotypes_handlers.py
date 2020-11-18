from unittest import TestCase, mock

from shapely.geometry import Polygon

from tests.dataset import wkt as wkt_dataset, shapely as shapely_dataset, geojson as geojson_dataset

from geosy import GeoFormats
from geosy.geotype_handlers import GeometryTypeConverter, Identifier, GeoTypesFactory
from geosy.geotypes import Wkt, GeoJson, GeoJsonPolygon, WktPolygon
from geosy.exceptions import UnsupportedGeoTypeError, UnsupportedShapeError


class TestGeometryTypeConverter(TestCase):

    def test_should_convert_shapely_polygon_to_wkt_polygon(self):
        factory_mock = mock.MagicMock()
        factory_mock.create_wkt.return_value = WktPolygon(wkt_dataset.POLYGON)

        shapely_polygon = shapely_dataset.POLYGON
        converter = GeometryTypeConverter(mock.MagicMock(), factory_mock)
        wkt_polygon = converter.from_shapely_to_wkt(shapely_polygon)
        self.assertIsInstance(wkt_polygon, Wkt)
        self.assertEqual(
            wkt_dataset.POLYGON,
            wkt_polygon.as_str
        )

    def test_should_convert_wkt_polygon_to_shapely_polygon(self):
        wkt_polygon = WktPolygon(wkt_dataset.POLYGON)
        converter = GeometryTypeConverter(mock.MagicMock(), mock.MagicMock())
        shapely_polygon = converter.from_wkt_to_shapely(wkt_polygon)
        self.assertIsInstance(shapely_polygon, Polygon)
        self.assertEqual(
            wkt_dataset.POLYGON,
            shapely_polygon.wkt
        )

    def test_should_convert_polygon_geometry_from_wkt_to_geojson_polygon(self):
        factory_mock = mock.MagicMock()
        factory_mock.create_geo_json.return_value = GeoJsonPolygon(geojson_dataset.POLYGON)

        wkt_polygon = Wkt(wkt_dataset.POLYGON)
        converter = GeometryTypeConverter(mock.MagicMock(), factory_mock)
        geojson = converter.from_wkt_to_geojson(wkt_polygon)
        self.assertIsInstance(geojson, GeoJson)
        self.assertEqual({'type': 'Polygon', 'coordinates': [[[-50.1715041, -21.7928566], [-50.1744239, -21.7924781], [-50.1773223, -21.7929562], [-50.1784601, -21.7950084], [-50.1723414, -21.7959647], [-50.1715041, -21.7928566]]]}, geojson.as_dict)

    def test_should_convert_from_unknown_to_spec_type(self):
        identifier_mock = mock.MagicMock()
        identifier_mock.identify_geo_type.return_value = GeoFormats.WKT
        wkt_polygon = WktPolygon(wkt_dataset.POLYGON)
        converter = GeometryTypeConverter(identifier_mock, mock.MagicMock())
        shapely_polygon = converter.from_unknown_to_spec_type(wkt_polygon, spec_type=GeoFormats.SHAPELY)
        self.assertIsInstance(shapely_polygon, Polygon)
        self.assertEqual(
            wkt_dataset.POLYGON,
            shapely_polygon.wkt
        )

    def test_convert_from_unknown_to_spec_type_should_raise_exception_when_unknown_type_is_not_valid(self):
        identifier_mock = mock.MagicMock()
        identifier_mock.identify_geo_type.side_effect = UnsupportedGeoTypeError
        unknown_type = mock.MagicMock()

        with self.assertRaises(UnsupportedGeoTypeError):
            converter = GeometryTypeConverter(identifier_mock, mock.MagicMock())
            converter.from_unknown_to_spec_type(unknown_type, spec_type=GeoFormats.SHAPELY)

    def test_convert_from_unknown_to_spec_type_should_raise_exception_when_spec_type_is_not_valid(self):
        wkt_polygon = WktPolygon(wkt_dataset.POLYGON)
        identifier_mock = mock.MagicMock()
        identifier_mock.identify_geo_type.side_effect = UnsupportedGeoTypeError

        with self.assertRaises(UnsupportedGeoTypeError):
            converter = GeometryTypeConverter(identifier_mock, mock.MagicMock())
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
        wkt_polygon = WktPolygon(wkt_dataset.POLYGON)
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

    def test_should_create_geojson_polygon(self):
        factory = GeoTypesFactory()
        geojso_polygon = factory.create_geo_json(geojson_dataset.POLYGON)
        self.assertIsInstance(geojso_polygon, GeoJsonPolygon)
        self.assertEqual(geojson_dataset.POLYGON, geojso_polygon.as_dict)

    def test_should_raise_UnsupportedShapeError_when_geojson_is_not_supported(self):
        factory = GeoTypesFactory()
        with self.assertRaises(UnsupportedShapeError):
            factory.create_geo_json(geojson_dataset.POINT)
