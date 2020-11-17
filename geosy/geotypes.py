from shapely import wkt
from shapely.errors import WKTReadingError

from geosy.exceptions import CorruptedGeometryError


class Wkt:

    def __init__(self, value_wkt: str):
        self.__wkt = value_wkt

        try:
            shapely_geometry = wkt.loads(self.__wkt)
        except WKTReadingError:
            raise CorruptedGeometryError(f'The wkt geometry {self.__wkt} is corrupted')

        self.__is_valid = shapely_geometry.is_valid

    def __str__(self):
        return self.__wkt

    @property
    def as_str(self) -> str:
        return self.__wkt

    @property
    def is_valid(self) -> bool:
        return self.__is_valid
