POLYGON = {
    "type": "Polygon",
    "coordinates": [
        [
            [100, 0],
            [101, 1],
            [100, 1],
            [100, 0]
        ]
    ]
}

POLYGON_CORRUPTED_WITH_STRING_INSTEAD_OF_NUMBER_IN_COORDINATES = {
    "type": "Polygon",
    "coordinates": [
        [
            [100, 'this string should not be here'],
            [101, 0],
            [101, 1],
            [100, 1],
            [100, 0]
        ]
    ]
}


POLYGON_INVALID_WITH_ONE_MORE_COORDINATE = {
    "type": "Polygon",
    "coordinates": [
        [
            [100, 0, 2],
            [101, 0],
            [101, 1],
            [100, 1],
            [100, 0]
        ]
    ]
}


POINT = {
    "type": "Point",
    "coordinates": [100, 0]
}