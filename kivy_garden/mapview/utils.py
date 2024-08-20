# coding=utf-8

__all__ = ["clamp", "haversine", "get_zoom_for_radius"]

from contextlib import suppress
from math import asin, cos, pi, radians, sin, sqrt, log, tan

from kivy.core.window import Window
from kivy.metrics import dp


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    Taken from: http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


def get_zoom_for_radius(radius_km, lat=None, tile_size=256.0):
    """See: https://wiki.openstreetmap.org/wiki/Zoom_levels"""
    radius = radius_km * 1000.0
    if lat is None:
        lat = 0.0  # Do not compensate for the latitude

    # Calculate the equatorial circumference based on the WGS-84 radius
    earth_circumference = 2.0 * pi * 6378137.0 * cos(lat * pi / 180.0)

    # Check how many tiles that are currently in view
    nr_tiles_shown = min(Window.size) / dp(tile_size)

    # Keep zooming in until we find a zoom level where the circle
    # can fit inside the screen
    zoom = 1
    with suppress(OverflowError):
        while (
            earth_circumference
            / (2 << (zoom - 1)) * nr_tiles_shown
            > 2 * radius
        ):
            zoom += 1
    return zoom - 1  # Go one zoom level back


def get_bounding_box(locations):
    """
    Calculate the minimum and maximum latitude and longitude
    from the given set of coordinates to form a bounding box

    :Parameters:
        `locations`: List of tuples containing latitude and longitude.
    """
    min_lat = min(locations, key=lambda x: x[0])[0]
    max_lat = max(locations, key=lambda x: x[0])[0]
    min_lon = min(locations, key=lambda x: x[1])[1]
    max_lon = max(locations, key=lambda x: x[1])[1]
    return min_lat, max_lat, min_lon, max_lon


def get_bounding_box_center(locations):
    """
    Find the center of this bounding box by averaging the
    minimum and maximum latitudes and longitudes

    :Parameters:
        `locations`: List of tuples containing latitude and longitude.
    """
    min_lat, max_lat, min_lon, max_lon = get_bounding_box(locations)
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2
    return center_lat, center_lon


def get_fit_zoom_level(locations, map_width, map_height, tile_size=256):
    """
    Calculates the zoom level to fit all locations into the map view.

    Determine the zoom level that fits the bounding box within the map view.
    This involves calculating the required scale to fit both the width
    and height of the bounding box into the viewport.

    :Parameters:
        `locations`: List of tuples containing latitude and longitude.
        `map_width`: Width of the map
        `map_height`: Height of the map

    :return: Calculated zoom level.
    """
    min_lat, max_lat, min_lon, max_lon = get_bounding_box(locations)

    # Function to convert latitude to pixel value
    def lat_to_pixel(lat, zoom):
        return (
            tile_size
            * (1 - log(tan(radians(lat)) + 1 / cos(radians(lat))) / pi)
            / 2 * (2 ** zoom)
        )

    # Function to convert longitude to pixel value
    def lon_to_pixel(lon, zoom):
        return tile_size * (lon + 180) / 360 * (2 ** zoom)

    # Determine the best zoom level
    zoom = 1
    for z in range(1, 21):  # Assuming a max zoom level of 20
        lat_pixel_range = lat_to_pixel(max_lat, z) - lat_to_pixel(min_lat, z)
        lon_pixel_range = lon_to_pixel(max_lon, z) - lon_to_pixel(min_lon, z)

        if lat_pixel_range < map_height and lon_pixel_range < map_width:
            zoom = z
        else:
            break

    return zoom


def update_map_view(
        map_width,
        map_height,
        lat1,
        lon1,
        lat2,
        lon2,
        mapview=None,
        polyline_layer=None,
        max_zoom=16,
        tile_size=256
):
    """
    Updates the MapView to ensure that two specified
    locations are both visible on the screen, centering the
    view between the two locations and adjusting the zoom level
    accordingly.

    This function calculates the optimal center point and zoom
    level for the MapView to display both `(lat1, lon1)` and `(lat2, lon2)`.
    It ensures that the map is centered between these two points and
    adjusts the zoom level so that both locations remain visible within
    the given map dimensions.

    The function performs the following steps:
    1. Calculates the geographic center between
        `(lat1, lon1)` and `(lat2, lon2)`.
    2. Determines the appropriate zoom level to fit both locations within
        the specified `map_width` and `map_height`.
    3. Further adjusts the zoom level based on the distance between the two
        locations using the Haversine formula.
    4. Centers the map on the calculated center point.
    5. Sets the zoom level to the average of the calculated zoom levels, with a
        maximum zoom level of 16.
    6. Updates the coordinates for the polyline layer to draw a line between
        `(lat1, lon1)` and `(lat2, lon2)`.

    """
    coordinates = [(lat1, lon1), (lat2, lon2)]
    center_lat, center_lon = get_bounding_box_center(coordinates)
    z1 = get_fit_zoom_level(
        coordinates,
        map_width,
        map_height,
        tile_size
    )
    z2 = get_zoom_for_radius(haversine(lon1, lat1, lon2, lat2))
    zoom_level = int((z1 + z2) / 2)
    if mapview:
        mapview.center_on(center_lat, center_lon)
        mapview.zoom = min(zoom_level, max_zoom)
    if polyline_layer:
        polyline_layer.coordinates = coordinates
    return (center_lat, center_lon), zoom_level


def generate_circle_points(lat, lon, radius, precision=360):
    """
    Generates a list of points that form a circle around a
    given latitude and longitude.

    The function calculates `N` points that form a circle with a
    specified radius aroundthe central point defined by the given
    latitude (`lat`) and longitude (`lon`).

    Args:
        lat (float): The latitude of the central point around
            which the circle is generated.
        lon (float): The longitude of the central point around
            which the circle is generated.
        radius (float): The radius of the circle in kilometers.
        precision (int, float): The precision of the circle

    Returns:
        list of dict: A list of dictionaries, where each dictionary contains
            latitude ('lat') and longitude ('lon') of a point on the circle.

    Example:
        >>> generate_circle_points(37.7749, -122.4194, 10)
        [{'lat': 37.78215, 'lon': -122.4194},
        {'lat': 37.78206, 'lon': -122.415}, ...]
    """

    # generate points
    circlePoints = []
    for k in range(precision):
        angle = pi * 2 * k / precision
        dx = radius * cos(angle)
        dy = radius * sin(angle)
        point = {
            'lat': lon + (180 / pi) * (dy / 6371),
            'lon': lat + (180 / pi) * (dx / 6371) / cos(lon * pi / 180)
        }
        # add to list
        circlePoints.append(point)

    return circlePoints
