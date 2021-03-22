from s2 import s2


def geotos2(latitude, longitude):
    """
    Convert latitude and longitufe to s2sphere with level 16
    :param latitude: latitiude of the location
    :param longitude: longitude of the location
    :return: s2sphere with level 16
    """
    level = 16
    return str(s2.geo_to_s2(latitude, longitude, level))
