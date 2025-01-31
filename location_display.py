import webbrowser

def decimal_to_dms(lat, lon):
    def convert(coord):
        degrees = int(coord)
        minutes = int((abs(coord) - abs(degrees)) * 60)
        seconds = (abs(coord) - abs(degrees) - minutes / 60) * 3600
        direction = ('N' if coord >= 0 else 'S') if 'lat' in locals() else ('E' if coord >= 0 else 'W')
        return f"{abs(degrees)}°{minutes}'{seconds:.1f}\"{direction}"

    return convert(lat), convert(lon)

def dms_to_decimal(dms_lat, dms_lon):
    def convert(dms):
        degrees, minutes, seconds, direction = int(dms[0]), int(dms[1]), float(dms[2]), dms[3]
        decimal = degrees + minutes / 60 + seconds / 3600
        return decimal if direction in ('N', 'E') else -decimal

    return convert(dms_lat), convert(dms_lon)

def open_map(lat, lon):
    url = f"https://www.google.com/maps?q={lat},{lon}"
    webbrowser.open(url)

# Example usage:
dec_lat, dec_lon = 38.869256523, -77.0535764524 # 41.40338, 2.17403
#dms_lat = (41, 24, 12.2, 'N')
#dms_lon = (2, 10, 26.5, 'E')
dms_lat = (38, 52, 9.32, 'N')
dms_lon = (77, 3, 12.88, 'W')

# Convert decimal to DMS
dms_coordinates = decimal_to_dms(dec_lat, dec_lon)
print("DMS Format:", dms_coordinates)

# Convert DMS to decimal
dec_coordinates = dms_to_decimal(dms_lat, dms_lon)
print("Decimal Format:", dec_coordinates)

# Open location in Google Maps
# open_map(dec_lat, dec_lon)

from IPython.display import display, HTML

def open_map_colab(lat, lon):
    url = f"https://www.google.com/maps?q={lat},{lon}"
    display(HTML(f'<a href="{url}" target="_blank">Open Google Maps</a>'))

# Example usage:
open_map_colab(dec_lat, dec_lon)

"""
DMS Format: ('38°52\'9.3"E', '77°3\'12.9"W')
Decimal Format: (38.869255555555554, -77.05357777777778)
url: Open Google Maps
"""

#!pip install pygeohash
import math
from typing import Tuple, Union
import pygeohash

def dd_to_dms(dec: float) -> Tuple[int, int, float, str]:
    """
    Convert decimal degrees to degrees, minutes, seconds

    Args:
        dec (float): Decimal degrees coordinate

    Returns:
        Tuple[int, int, float, str]: (degrees, minutes, seconds, direction)
    """
    direction = 'N' if dec >= 0 else 'S' if dec < 0 and abs(dec) <= 90 else 'E' if dec >= 0 else 'W'
    dec = abs(dec)
    degrees = int(dec)
    minutes = int((dec - degrees) * 60)
    seconds = round(((dec - degrees) * 60 - minutes) * 60, 2)
    return (degrees, minutes, seconds, direction)

def dms_to_dd(degrees: int, minutes: int, seconds: float, direction: str) -> float:
    """
    Convert degrees, minutes, seconds to decimal degrees

    Args:
        degrees (int): Degrees
        minutes (int): Minutes
        seconds (float): Seconds
        direction (str): One of N, S, E, W

    Returns:
        float: Decimal degrees
    """
    dd = degrees + minutes/60 + seconds/3600
    if direction.upper() in ['S', 'W']:
        dd = -dd
    return dd

def coordinates_to_geohash(lat: float, lon: float, precision: int = 12) -> str:
    """
    Convert decimal degree coordinates to geohash

    Args:
        lat (float): Latitude in decimal degrees
        lon (float): Longitude in decimal degrees
        precision (int): Length of resulting geohash

    Returns:
        str: Geohash string
    """
    return pygeohash.encode(lat, lon, precision=precision)

def geohash_to_coordinates(geohash: str) -> Tuple[float, float]:
    """
    Convert geohash to decimal degree coordinates

    Args:
        geohash (str): Geohash string

    Returns:
        Tuple[float, float]: (latitude, longitude) in decimal degrees
    """
    return pygeohash.decode(geohash)

def dd_to_utm(latitude: float, longitude: float) -> Tuple[int, float, float, str]:
    """
    Convert decimal degrees to UTM coordinates

    Args:
        latitude (float): Latitude in decimal degrees
        longitude (float): Longitude in decimal degrees

    Returns:
        Tuple[int, float, float, str]: (zone number, easting, northing, zone letter)
    """
    # Constants
    k0 = 0.9996  # scale factor
    a = 6378137  # WGS84 equatorial radius
    e = 0.081819190842622  # WGS84 eccentricity

    # Calculate UTM zone
    zone_number = int((longitude + 180) / 6) + 1

    # Convert to radians
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)

    # Calculate zone central meridian
    central_lon = math.radians(-183 + (zone_number * 6))

    # Get zone letter
    if 84 >= latitude >= 72: zone_letter = 'X'
    elif 72 > latitude >= 64: zone_letter = 'W'
    elif 64 > latitude >= 56: zone_letter = 'V'
    elif 56 > latitude >= 48: zone_letter = 'U'
    elif 48 > latitude >= 40: zone_letter = 'T'
    elif 40 > latitude >= 32: zone_letter = 'S'
    elif 32 > latitude >= 24: zone_letter = 'R'
    elif 24 > latitude >= 16: zone_letter = 'Q'
    elif 16 > latitude >= 8: zone_letter = 'P'
    elif 8 > latitude >= 0: zone_letter = 'N'
    elif 0 > latitude >= -8: zone_letter = 'M'
    elif -8 > latitude >= -16: zone_letter = 'L'
    elif -16 > latitude >= -24: zone_letter = 'K'
    elif -24 > latitude >= -32: zone_letter = 'J'
    elif -32 > latitude >= -40: zone_letter = 'H'
    elif -40 > latitude >= -48: zone_letter = 'G'
    elif -48 > latitude >= -56: zone_letter = 'F'
    elif -56 > latitude >= -64: zone_letter = 'E'
    elif -64 > latitude >= -72: zone_letter = 'D'
    elif -72 > latitude >= -80: zone_letter = 'C'
    else: zone_letter = 'Z'

    # Equations
    e_squared = e * e
    e_prime_squared = e_squared / (1 - e_squared)

    n = a / math.sqrt(1 - e_squared * math.sin(lat_rad) * math.sin(lat_rad))
    t = math.tan(lat_rad) * math.tan(lat_rad)
    c = e_prime_squared * math.cos(lat_rad) * math.cos(lat_rad)
    A = math.cos(lat_rad) * (lon_rad - central_lon)

    # Calculate M
    M = a * ((1 - e_squared/4 - 3*e_squared*e_squared/64 - 5*e_squared*e_squared*e_squared/256) * lat_rad -
             (3*e_squared/8 + 3*e_squared*e_squared/32 + 45*e_squared*e_squared*e_squared/1024) * math.sin(2*lat_rad) +
             (15*e_squared*e_squared/256 + 45*e_squared*e_squared*e_squared/1024) * math.sin(4*lat_rad) -
             (35*e_squared*e_squared*e_squared/3072) * math.sin(6*lat_rad))

    # Calculate UTM coordinates
    easting = k0 * n * (A + (1-t+c) * A*A*A/6 + (5-18*t+t*t+72*c-58*e_prime_squared) * A*A*A*A*A/120) + 500000
    northing = k0 * (M + n * math.tan(lat_rad) * (A*A/2 + (5-t+9*c+4*c*c) * A*A*A*A/24 +
                                                 (61-58*t+t*t+600*c-330*e_prime_squared) * A*A*A*A*A*A/720))

    # Adjust northing for southern hemisphere
    if latitude < 0:
        northing += 10000000

    return (zone_number, easting, northing, zone_letter)

def format_dms(dms: Tuple[int, int, float, str]) -> str:
    """
    Format DMS tuple as string

    Args:
        dms (Tuple[int, int, float, str]): (degrees, minutes, seconds, direction)

    Returns:
        str: Formatted DMS string
    """
    return f"{dms[0]}°{dms[1]}'{dms[2]}\"{dms[3]}"

# Example usage
if __name__ == "__main__":
    # Test coordinates (Washington Monument)
    dec_lat, dec_lon = 38.869256523, -77.0535764524

    # Convert DD to DMS
    dms_lat = dd_to_dms(dec_lat)
    dms_lon = dd_to_dms(dec_lon)
    print(f"DMS: {format_dms(dms_lat)} {format_dms(dms_lon)}")

    # Convert to GEOHASH
    geohash = coordinates_to_geohash(dec_lat, dec_lon)
    print(f"GEOHASH: {geohash}")

    # Convert to UTM
    zone_number, easting, northing, zone_letter = dd_to_utm(dec_lat, dec_lon)
    print(f"UTM: {zone_number}{zone_letter} {int(easting)}E {int(northing)}N")

"""
DMS: 38°52'9.32"N 77°3'12.88"S
GEOHASH: dqcjnegmcd94
UTM: 18S 321842E 4304272N
"""