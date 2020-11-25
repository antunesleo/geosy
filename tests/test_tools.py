from unittest import TestCase, mock

from shapely.geometry import Polygon

from tests.datasets import wkt_str_dataset as wkt_dataset
from tests.datasets import shapely_dataset as shapely_dataset
from tests.datasets import geojson_dict_dataset as geojson_dataset

from geosy.geometries import GeoFormats
from geosy.tools import GeometryTypeConverter, is_geometry_valid
from geosy.tools import identify_geometry_type, create_geo_json, create_wkt
from geosy.geometries import Wkt, GeoJson, GeoJsonPolygon, WktPolygon
from geosy.exceptions import UnsupportedGeoTypeError, UnsupportedShapeError, UnsupportedError


class TestIdentifyGeoType(TestCase):

    def test_should_identify_shapely_geo_type(self):
        geotype = identify_geometry_type(shapely_dataset.POLYGON)
        self.assertEqual(GeoFormats.SHAPELY, geotype)

    def test_should_identify_wkt_geo_type(self):
        wkt_polygon = WktPolygon(wkt_dataset.POLYGON)
        geotype = identify_geometry_type(wkt_polygon)
        self.assertEqual(GeoFormats.WKT, geotype)

    def test_should_raise_unsupported_geotype(self):
        unsupported_type = mock.MagicMock()
        with self.assertRaises(UnsupportedGeoTypeError):
            identify_geometry_type(unsupported_type)


class TestGeometryTypeConverter(TestCase):

    def test_should_convert_shapely_polygon_to_wkt_polygon(self):
        factory_mock = mock.MagicMock()
        factory_mock.create_wkt.return_value = WktPolygon(wkt_dataset.POLYGON)

        shapely_polygon = shapely_dataset.POLYGON
        converter = GeometryTypeConverter()
        wkt_polygon = converter.from_shapely_to_wkt(shapely_polygon)
        self.assertIsInstance(wkt_polygon, Wkt)
        self.assertEqual(wkt_dataset.POLYGON, wkt_polygon.as_str)

    def test_should_convert_wkt_polygon_to_shapely_polygon(self):
        wkt_polygon = WktPolygon(wkt_dataset.POLYGON)
        converter = GeometryTypeConverter()
        shapely_polygon = converter.from_wkt_to_shapely(wkt_polygon)
        self.assertIsInstance(shapely_polygon, Polygon)
        self.assertEqual(wkt_dataset.POLYGON, shapely_polygon.wkt)

    def test_should_convert_polygon_geometry_from_wkt_to_geojson_polygon(self):
        wkt_polygon = Wkt(wkt_dataset.POLYGON)
        converter = GeometryTypeConverter()
        geojson = converter.from_wkt_to_geojson(wkt_polygon)
        self.assertIsInstance(geojson, GeoJson)
        self.assertEqual({'type': 'Polygon', 'coordinates': [[[-50.1715041, -21.7928566], [-50.1744239, -21.7924781], [-50.1773223, -21.7929562], [-50.1784601, -21.7950084], [-50.1723414, -21.7959647], [-50.1715041, -21.7928566]]]}, geojson.as_dict)

    def test_should_convert_from_unknown_to_spec_type(self):
        wkt_polygon = WktPolygon(wkt_dataset.POLYGON)
        converter = GeometryTypeConverter()
        shapely_polygon = converter.from_unknown_to_spec_type(wkt_polygon, spec_type=GeoFormats.SHAPELY)
        self.assertIsInstance(shapely_polygon, Polygon)
        self.assertEqual(wkt_dataset.POLYGON, shapely_polygon.wkt)

    def test_convert_from_unknown_to_spec_type_should_raise_exception_when_unknown_type_is_not_valid(self):
        unknown_type = mock.MagicMock()
        converter = GeometryTypeConverter()

        with self.assertRaises(UnsupportedGeoTypeError):
            converter.from_unknown_to_spec_type(unknown_type, spec_type=GeoFormats.SHAPELY)

    def test_convert_from_unknown_to_spec_type_should_return_unkown_when_is_equal_to_spec(self):
        converter = GeometryTypeConverter()
        geometry = converter.from_unknown_to_spec_type(shapely_dataset.POLYGON, GeoFormats.SHAPELY)
        self.assertEqual(geometry, shapely_dataset.POLYGON)

    def test_should_convert_polygon_from_shapely_to_geojson(self):
        converter = GeometryTypeConverter()
        geojson_polygon = converter.from_shapely_to_geojson(shapely_dataset.POLYGON)
        self.assertIsInstance(geojson_polygon, GeoJsonPolygon)
        self.assertEqual(geojson_polygon.as_dict, geojson_dataset.POLYGON)

    def test_should_convert_polygon_from_geojson_to_shapely(self):
        converter = GeometryTypeConverter()
        shapely_polygon = converter.from_geojson_to_shapely(create_geo_json(geojson_dataset.POLYGON))
        self.assertIsInstance(shapely_polygon, Polygon)
        self.assertEqual(shapely_polygon.wkt, shapely_dataset.POLYGON.wkt)


class TestIsGeometryValid(TestCase):

    def test_is_geometry_valid_should_return_if_polygon_wkt_geometry_is_valid(self):
        wkt_polygon = WktPolygon(wkt_dataset.POLYGON)
        self.assertTrue(is_geometry_valid(wkt_polygon))

    def test_is_geometry_valid_should_return_if_geojson_polygon_geometry_is_valid(self):
        geojson_polygon = GeoJsonPolygon(geojson_dataset.POLYGON)
        self.assertTrue(is_geometry_valid(geojson_polygon))

    def test_is_geometry_valid_should_raise_UnsupportedTypeError_when_the_geo_type_is_not_supported(self):
        not_supported_type = mock.MagicMock()
        with self.assertRaises(UnsupportedError):
            is_geometry_valid(not_supported_type)


class TestCreateWkt(TestCase):

    def test_should_create_wkt_polygon(self):
        polygon_wkt = create_wkt(wkt_dataset.POLYGON)
        self.assertIsInstance(polygon_wkt, WktPolygon)
        self.assertEqual(wkt_dataset.POLYGON, polygon_wkt.as_str)

    def test_should_raise_UnsupportedShapeError_when_shape_is_not_supported(self):
        with self.assertRaises(UnsupportedShapeError):
            create_wkt(wkt_dataset.POINT)


class TestCreateGeoJsonFactory(TestCase):

    def test_should_create_geojson_polygon(self):
        geojso_polygon = create_geo_json(geojson_dataset.POLYGON)
        self.assertIsInstance(geojso_polygon, GeoJsonPolygon)
        self.assertEqual(geojson_dataset.POLYGON, geojso_polygon.as_dict)

    def test_should_raise_UnsupportedShapeError_when_geojson_is_not_supported(self):
        with self.assertRaises(UnsupportedShapeError):
            create_geo_json(geojson_dataset.POINT)