from pathlib import Path
import math
import json
import pandas as pd
import os
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


base_path = "geojson"
northMin = 337
northMax = 22
northMinVal = 360
northMaxVal = 0
northMinCoord = None
northMaxCoord = None

eastMin = 67
eastMax = 112
eastMinVal = 112
eastMaxVal = 67
eastMinCoord = None
eastMaxCoord = None

southMin = 157.5
southMax = 202.5
southMinVal = 202.5
southMaxVal = 157.5
southMinCoord = None
southMaxCoord = None

westMin = 247
westMax = 292
westMinVal = 292
westMaxVal = 247
westMinCoord = None
westMaxCoord = None

northEastMin = 22
northEastMax = 67
northEastMinVal = 67
northEastMaxVal = 22
northEastMinCoord = None
northEastMaxCoord = None


southEastMin = 112
southEastMax = 157
southEastMinVal = 157
southEastMaxVal = 112
southEastMinCoord = None
southEastMaxCoord = None


northWestMin = 292
northWestMax = 337
northWestMinVal = 337
northWestMaxVal = 292
northWestMinCoord = None
northWestMaxCoord = None


southWestMin = 202
southWestMax = 247
southWestMinVal = 247
southWestMaxVal = 202
southWestMinCoord = None
southWestMaxCoord = None

north = []
south = []
east = []
west = []
northEast = []
southEast = []
northWest = []
southWest = []
centeral = []

def calculate_bearing(pointA, pointB):
  
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        return 400
    if (type(pointB[0]) != float) or (type(pointB[0]) != float):
        return 400
    
    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

  
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def ensure_dir(country, city, isCountry):
    path = ''
    if isCountry:
        path = base_path+ os.path.sep+  country.lower()+os.path.sep
    else:
        path = base_path+ os.path.sep+  country.lower() + os.path.sep + "cities"+ os.path.sep + city.lower() +os.path.sep
    directory = os.path.dirname(path)
    
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except Exception as e:   
        print(e)
    return path    

def midpoint(x1, y1, x2, y2, angle):
    
    lonA = math.radians(y1)
    lonB = math.radians(y2)
    latA = math.radians(x1)
    latB = math.radians(x2)

    dLon = lonB - lonA

    Bx = math.cos(latB) * math.cos(dLon)
    By = math.cos(latB) * math.sin(dLon)

    latC = math.atan2(math.sin(latA) + math.sin(latB),
                  math.sqrt((math.cos(latA) + Bx) * (math.cos(latA) + Bx) + By * By))
    lonC = lonA + math.atan2(By, math.cos(latA) + Bx)
    lonC = (lonC + 3 * math.pi) % (2 * math.pi) - math.pi
    latitude = round(math.degrees(latC), 6)
    longitude = round(math.degrees(lonC),6)
    return [latitude, longitude, angle]


def setGeoJson(arr, id, centroid, path, cardinal):
    cardinal_json = {}
    cardinal_json['type'] = 'FeatureCollection'
    cardinal_json['features'] = []
    coordinates_cardinal= []
    coordinates_cardinal.append(arr)

    cardinal_json['features'].append({
    'type':'Feature',
    'id': id,
    'properties': {
        'centroid': centroid
        },
    'geometry': {
        'type':'Polygon',
        'coordinates': coordinates_cardinal     
        }
    })
    with open(path +cardinal+'.geojson', 'w') as outfile:
        json.dump(cardinal_json, outfile)


centroid = (3.8767337,43.6112422)
df = pd.read_csv('cities.csv')
df = df.loc[(df['country'] == 'FR') & (df['name'] == 'Paris')]
for index, row in df.iterrows():
    path = ensure_dir(row['country'], row['name'], False)
    request_url = 'https://nominatim.openstreetmap.org/search.php?q='+row['name'].lower()+'&polygon_geojson=1&accept-language=en&format=jsonv2'
    #print(request_url)
    page = requests.get(request_url, verify=False)
    json_content = json.loads(page.content)
    if len(json_content) > 0:
        centroid = (float(json_content[0]['lon']), float(json_content[0]['lat']))
        print(str(centroid))
        all_coordinates = []
        print(json_content[0]['geojson']['type'])
        if json_content[0]['geojson']['type'] == 'MultiPolygon':
            for coordinate in json_content[0]['geojson']['coordinates']:
                all_coordinates.extend(coordinate[0])
        else:
            all_coordinates = json_content[0]['geojson']['coordinates'][0] 
        #print("Polygon:"+str(all_coordinates))    
        for p in all_coordinates:
            p2 = (p[0], p[1])
            angle = calculate_bearing(centroid, p2)
            p.append(angle)
            northMin = 337
            northMax = 22
            northMinVal = 360
            northMaxVal = 0
            if angle >= northMin or angle <= northMax:
                north.append(p)
            if angle >= southMin and angle <= southMax:
                south.append(p) 
            if angle >= eastMin and angle <= eastMax:
                east.append(p)  
            if angle >= westMin and angle <= westMax:
                west.append(p)  
            if angle >= northEastMin and angle <= northEastMax:
                northEast.append(p)  
            if angle >= southEastMin and angle <= southEastMax:
                southEast.append(p)  
            if angle >= northWestMin and angle <= northWestMax:
                northWest.append(p) 
            if angle >= southWestMin and angle <= southWestMax:
                southWest.append(p) 
                
                
north.sort(key=lambda k: k[2])  
south.sort(key=lambda k: k[2])  
east.sort(key=lambda k: k[2])  
west.sort(key=lambda k: k[2]) 
northEast.sort(key=lambda k: k[2])  
northWest.sort(key=lambda k: k[2])     
southEast.sort(key=lambda k: k[2])  
southWest.sort(key=lambda k: k[2])   

p1North = midpoint(centroid[0], centroid[1], north[0][0], north[0][1], north[0][2])
p2North = midpoint(centroid[0], centroid[1], north[-1][0], north[-1][1], north[-1][2])
north.append(p2North)
north.append(p1North)

p1East = midpoint(centroid[0], centroid[1], east[0][0], east[0][1], east[0][2])
p2East = midpoint(centroid[0], centroid[1], east[-1][0], east[-1][1], east[-1][2])
east.append(p2East)
east.append(p1East)

p1NorthEast = midpoint(centroid[0], centroid[1], northEast[0][0], northEast[0][1], northEast[0][2])
p2NorthEast = midpoint(centroid[0], centroid[1], northEast[-1][0], northEast[-1][1], northEast[-1][2])
northEast.append(p2NorthEast)
northEast.append(p1NorthEast)

p1NorthWest = midpoint(centroid[0], centroid[1], northWest[0][0], northWest[0][1], northWest[0][2])
p2NorthWest = midpoint(centroid[0], centroid[1], northWest[-1][0], northWest[-1][1], northWest[-1][2])
northWest.append(p2NorthWest)
northWest.append(p1NorthWest)
       
p1South = midpoint(centroid[0], centroid[1], south[0][0], south[0][1], south[0][2])
p2South = midpoint(centroid[0], centroid[1], south[-1][0], south[-1][1], south[-1][2])
south.append(p2South)
south.append(p1South)

p1West = midpoint(centroid[0], centroid[1], west[0][0], west[0][1], west[0][2])
p2West = midpoint(centroid[0], centroid[1], west[-1][0], west[-1][1], west[-1][2])
west.append(p2West)                 
west.append(p1West)    

p1SouthEast = midpoint(centroid[0], centroid[1], southEast[0][0], southEast[0][1], southEast[0][2])
p2SouthEast = midpoint(centroid[0], centroid[1], southEast[-1][0], southEast[-1][1], southEast[-1][2])
southEast.append(p2SouthEast)
southEast.append(p1SouthEast)

p1SouthWest = midpoint(centroid[0], centroid[1], southWest[0][0], southWest[0][1], southWest[0][2])
p2SouthWest = midpoint(centroid[0], centroid[1], southWest[-1][0], southWest[-1][1], southWest[-1][2])
southWest.append(p2SouthWest)
southWest.append(p1SouthWest)


centeral.append(p2North)
centeral.append(p1North)
centeral.append(p2West)
centeral.append(p1West)
centeral.append(p2South)
centeral.append(p1South)
centeral.append(p2East)
centeral.append(p1East)

setGeoJson(north, json_content[0]['place_id'],centroid, path, 'north')
setGeoJson(south, json_content[0]['place_id'],centroid, path, 'south')
setGeoJson(east, json_content[0]['place_id'],centroid, path, 'east')
setGeoJson(west, json_content[0]['place_id'],centroid, path, 'west')
setGeoJson(northEast, json_content[0]['place_id'],centroid, path, 'north-east')
setGeoJson(southEast, json_content[0]['place_id'],centroid, path, 'south-east')
setGeoJson(southWest, json_content[0]['place_id'],centroid, path, 'south-west')
setGeoJson(northWest, json_content[0]['place_id'],centroid, path, 'north-west')
        
setGeoJson(centeral, json_content[0]['place_id'],centroid, path, 'centeral')
        
        
        

