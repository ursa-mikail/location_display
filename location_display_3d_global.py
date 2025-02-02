#!pip install geopy
from geopy.geocoders import Nominatim
import geopy

# Set the user agent
user_agent = "my-application"
# Set the default user agent for geopy
geopy.geocoders.options.default_user_agent = user_agent
# Initialize a Nominatim geocoder
# global:
geolocator = Nominatim(user_agent="http") # Nominatim(user_agent=user_agent)

def get_latitude_longitude(address):
    # Use the geocode function to get the location object
    location = geolocator.geocode(address)

    latitude = 0
    longitude = 0

    if location is None:
        print("Unable to geocode the address.")
    else:
        # Extract the latitude and longitude coordinates from the location object
        latitude = location.latitude
        longitude = location.longitude
        print(f"Latitude: {latitude}, Longitude: {longitude}")

    return latitude, longitude

def get_address(latitude, longitude):
    # Use the reverse method of the geolocator to get the location object
    location = geolocator.reverse(f"{latitude}, {longitude}")
    # Extract the formatted address from the location object
    address = location.address
    print(f"Address: {address}")
    return address

lat = []
lon = []
# addresses to geocode
addresses = ['1600 Amphitheatre Parkway, Mountain View, CA',
             'Ault Drive, Ingleside, South Stormont, Stormont, Dundas and Glengarry Counties, Eastern Ontario, Ontario, K0C 1M0, Canada',
             '1, Potters Alley, Fredericktown Hill, East Bethlehem Township, Washington County, Pennsylvania, 15333, United States',
             'Sutton Bay, Ontario P0J 1P0, Canada']
latitude, longitude = get_latitude_longitude(addresses[0])

print(f"{get_address(latitude, longitude)}")
print(f"{get_address(45, -75)}")
print(f"{get_address(40, -80)}")
print(f"{get_address(35, -85)}")

for i in range(0, len(addresses)):
  latitude, longitude = get_latitude_longitude(addresses[i])
  lat.append(latitude)
  lon.append(longitude)

#!pip install datapane
import plotly.graph_objs as go

# create a scattergeo trace
trace = go.Scattergeo(
    #lon = [-75, -80, -85, -122.08558456613565], # longitude coordinates of the data points
    #lat = [45, 40, 35, 37.42248575],            # latitude coordinates of the data points
    lon = lon,
    lat = lat,
    mode = 'markers',
    marker = dict(
        size = 10,
        color = 'red',
        line = dict(
            width = 2,
            color = 'black'
        )
    )
)

# create a layout for the map
layout = go.Layout(
    geo = dict(
        scope = 'world',  # set the scope of the map, e.g. north america
        projection = dict(type='orthographic'), # set the projection of the map
        showland = True,
        landcolor = 'rgb(243, 243, 243)',
        countrycolor = 'rgb(204, 204, 204)',
        coastlinecolor = 'rgb(255, 255, 255)',
        showcountries=True,
        showocean=True,
        oceancolor='rgb(0,0,255)',
        showlakes=True,
        lakecolor='rgb(0,255,255)',
        showrivers=True,
        rivercolor='rgb(0,0,255)',
    ),
)


fig = go.Figure(data=[trace], layout=layout)
fig.show()

import folium
import datapane as dp
from geopy.distance import geodesic
"""
# Create a Folium map centered on the location
m = folium.Map(location=[latitude, longitude]) #, zoom_start=13)
# Add a marker to the map
folium.Marker(location=[latitude, longitude]).add_to(m)
"""
location_1 = 0
location_2 = 1
distance = geodesic([lat[location_1], lon[location_1]], [lat[location_2], lon[location_2]]).km
print(f"Click on map of the 2nd location to see the same: The distance between {addresses[location_1]} and {addresses[location_2]} is {distance:.2f} kilometers")

m = folium.Map(location=[lat[0], lon[0]]) #
for i in range(0, len(addresses)):
    folium.Marker(location=[lat[i], lon[i]], tooltip = addresses[i]).add_to(m)

# Add a marker for each location
folium.Marker(location=[lat[location_1], lon[location_1]], tooltip=addresses[location_1]).add_to(m)
folium.Marker(location=[lat[location_2], lon[location_2]], tooltip=addresses[location_2],
              popup=f"Distance: {geodesic([lat[location_1], lon[location_1]], [lat[location_2], lon[location_2]]).km:.2f} km").add_to(m)

dp.Plot(m)

# https://docs.datapane.com/reference/display-blocks/plots/#plotly

"""
Latitude: 37.42248575, Longitude: -122.08558456613565
Address: Google Building 41, 1600, Amphitheatre Parkway, Mountain View, Santa Clara County, California, 94043, United States
Google Building 41, 1600, Amphitheatre Parkway, Mountain View, Santa Clara County, California, 94043, United States
Address: Ault Drive, Ingleside, South Stormont, Stormont, Dundas and Glengarry Counties, Eastern Ontario, Ontario, K0C 1M0, Canada
Ault Drive, Ingleside, South Stormont, Stormont, Dundas and Glengarry Counties, Eastern Ontario, Ontario, K0C 1M0, Canada
Address: 1, Potters Alley, Fredericktown Hill, East Bethlehem Township, Washington County, Pennsylvania, 15333, United States
1, Potters Alley, Fredericktown Hill, East Bethlehem Township, Washington County, Pennsylvania, 15333, United States
Address: Howardville, Hamilton County, East Tennessee, Tennessee, United States
Howardville, Hamilton County, East Tennessee, Tennessee, United States
Latitude: 37.42248575, Longitude: -122.08558456613565
WARNING:urllib3.connectionpool:Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ReadTimeoutError("HTTPSConnectionPool(host='nominatim.openstreetmap.org', port=443): Read timed out. (read timeout=1)")': /search?q=Ault+Drive%2C+Ingleside%2C+South+Stormont%2C+Stormont%2C+Dundas+and+Glengarry+Counties%2C+Eastern+Ontario%2C+Ontario%2C+K0C+1M0%2C+Canada&format=json&limit=1
Latitude: 44.995953771859384, Longitude: -74.99785574875088
Latitude: 39.999996, Longitude: -79.999961
Latitude: 47.5678311, Longitude: -79.5889826
"""