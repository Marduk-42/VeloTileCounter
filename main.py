from math import *
from shapely.geometry import Polygon, MultiPolygon
from fastkml import kml

#Download KMZ files from https://gadm.org/download_country.html
#and extract the KML file

#------------------------------
#Taken from:
#https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - asinh(tan(lat_rad)) / pi) / 2.0 * n)
  return (xtile, ytile)

#------------------------------
#Taken from:
#https://svn.openstreetmap.org/applications/routing/pyroute/tilenames.py
def mercatorToLat(mercatorY):
  return(degrees(atan(sinh(mercatorY))))

def latEdges(y,z=14):
  n = pow(2,z)
  unit = 1 / n
  relY1 = y * unit
  relY2 = relY1 + unit
  lat1 = mercatorToLat(pi * (1 - 2 * relY1))
  lat2 = mercatorToLat(pi * (1 - 2 * relY2))
  return(lat1,lat2)

def lonEdges(x,z=14):
  n = pow(2,z)
  unit = 360 / n
  lon1 = -180 + x * unit
  lon2 = lon1 + unit
  return(lon1,lon2)

#Coordinates of tile  
def tileEdges(x,y,z=14):
  lat1,lat2 = latEdges(y,z)
  lon1,lon2 = lonEdges(x,z)
  return((lat2, lon1, lat1, lon2)) #South, West, North, East


#------------------------------
#Not taken from anywhere

#Generate tiles from given point South-West (x,y) to North-East (lat, lon)
def tile_generator(x,y,lat,lon,z=14):
    tiles = []
    dx,dy = deg2num(x,y,z)
    lx,ly = deg2num(lat,lon,z)
    for tile_x in range(dx,lx+1):
        for tile_y in range(ly,dy+1):
            s,w,n,e = tileEdges(tile_x,tile_y,z)
            tiles.append(Polygon([(w,s),(e,s),(e,n),(w,n)]))
    return tiles

def extract_gadm_borders(path):
    #Extract borders from gadm.org
    file = open(path,'rb').read()
    k = kml.KML()
    k.from_string(file)
    f = list(k.features())[0]
    ff = list(f.features())[0]
    fff = list(ff.features())
    return [(el.geometry, el.extended_data.elements[0].data[-1]['value']) for el in fff]

def get_extreme_points(geometry):
    points = []
    if isinstance(geometry,MultiPolygon):
        for polygon in geometry.geoms:
            points.extend(polygon.exterior.coords[:-1])
    elif isinstance(geometry,Polygon):
        points = geometry.exterior.coords[:-1]
    else:
        raise Exception("Invalid geometry!")
    xlist = [point[0] for point in points]
    ylist = [point[1] for point in points]
    #S, W, N, E
    return [min(ylist), min(xlist), max(ylist), max(xlist)]

def count_tiles(path):
    borders = extract_gadm_borders(path)
    for data in borders:
        border, name = data
        print(name,end=", ")
        tiles = tile_generator(*get_extreme_points(border))
        counter = 0
        #Use the following if you want a progress bar:
        #from tqdm import tqdm
        #for element in tqdm(tiles)
        for element in tiles:
            if border.intersects(element):
                counter += 1
        print(counter)

path = "" #Insert path of file
count_tiles(path)

