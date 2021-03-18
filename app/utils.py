from s2 import s2


def geotos2(latitude, longitude):
    """

    :return:
    """

    level = 16
    return str(s2.geo_to_s2(latitude, longitude, level))
