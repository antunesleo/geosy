class Wkt:

    def __init__(self, value_wkt: str):
        self.__value_wkt = value_wkt

    @property
    def as_str(self) -> str:
        return self.__value_wkt
