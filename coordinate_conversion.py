import re

# This file converts the coordinates for selected nodes from DMS to decimal so that we can use them with OSM

def dms_to_decimal(coord):

    #if the user sends a coordinate that is any other type return it without change
    if not isinstance(coord, str):
        return coord
    
    try:
        latitude_string, longitude_string = coord.split()
        latitude = re.match(r"(\d+)°(\d+)'(\d+)\"([NS])", latitude_string)
        longitude = re.match(r"(\d+)°(\d+)'(\d+)\"([EW])", longitude_string)

        #if they dont match the format then return the coordinate as it was sent
        if not (latitude and longitude):
            return coord
        def convert(match):
            degrees, minutes, second, hemisphere = match.groups()
            decimal_val = float(degrees) + float(minutes) / 60.0 + float(second) / 3600.0
            
            if hemisphere in ("S", "W"):
                decimal_val = -decimal_val
            return decimal_val
        return (convert(latitude), convert(longitude))
    except Exception:
        return coord