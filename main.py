from math import *
from shapely.geometry import Polygon, MultiPolygon
from fastkml import kml
#Download KMZ files from https://gadm.org/download_country.html
#and extract the KML file

__version__ = '1.0'

MAX_LATITUDE = 85.0511287798 #degrees(arctan(sinh(pi)))

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

#Divide tile into four smaller tiles
def divide_tile(x,y,z):
    z += 1
    x *= 2
    y *= 2
    return ((x,y,z),(x+1,y,z),(x,y+1,z),(x+1,y+1,z))
  
def tileToPolygon(x,y,z):
    s,w,n,e=tileEdges(x,y,z)
    return Polygon([(w,s),(e,s),(e,n),(w,n)])

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

#Extract borders from gadm.org
def extract_gadm_borders(path):
    file = open(path,'rb').read()
    k = kml.KML()
    k.from_string(file) #In case this throws an error, try using other encodings
    f = list(k.features())[0]
    ff = list(f.features())[0]
    fff = list(ff.features())
    return [(el.geometry, el.extended_data.elements[0].data[-1]['value']) for el in fff]
  
#Get the northern/southern/western/easternmost point of the area
def get_extreme_points(geometry):
    #West, South, East, North
    w, s, e, n = geometry.bounds
    if abs(n) > MAX_LATITUDE or abs(s) > MAX_LATITUDE:
        print("Maximum latitude exceeded. No tiles up there")
    return [s,w,n,e]

#Former count tiles function
#Gives a better progress estimation, but takes longer
def _count_tiles(path):
    print("Deprecated!")
    borders = extract_gadm_borders(path)
    for data in borders:
        border, name = data
        print(name,end=", ")
        tiles = tile_generator(*get_extreme_points(border))
        counter = 0
        #Use the following if you want a progress bar:
        #from tqdm import tqdm
        #counter = tqdm(map(border.intersects, tiles), total=len(tiles))
        counter = tqdm(map(border.intersects, tiles), total=len(tiles))
        print(list(counter).count(1))
     
#Count tiles
#path: Path to file
#names: Only count these areas (if there are several areas)
#skip_names: Skip these areas (if there are several areas)
def count_tiles(path, names=[], skip_names=[], down_to=14):
    borders = extract_gadm_borders(path)
    for data in borders:
        tiles = [(0, 0, 1), (1, 0, 1),
                 (0, 1, 1), (1, 1, 1)] #Level 1 tiles
        counter = 0
        border, name = data
        if (name not in names and len(names)!=0) or name in skip_names:
            continue
        print(name,end=", ")
        while len(tiles) > 0:
            removing = []
            adding = []
            #Use 'for tile in tqdm(tiles)' if you want a progress bar for every zoom level
            for tile in tiles:
                polygon = tileToPolygon(*tile)
                #Calculate the shared area between a tile and the border
                area = border.intersection(polygon).area
                #If there whole area of the tile is inside the border, add the number of Level 14 tiles inside
                if isclose(polygon.area, area):
                    counter += pow(2,2*(down_to-tile[2]))
                #If only a bit of the area is inside
                elif not isclose(area,0):
                    #If the tile reached the maximum zoom level
                    if tile[2] == down_to:
                        counter += 1
                    else:
                        #Divide the tile into four smaller tiles (one zoom level higher/lower)
                        adding.extend(divide_tile(*tile))
                removing.append(tile)
            for element in removing:
                tiles.remove(element)
            tiles.extend(adding)
        print(round(counter))
        
path = "" #Insert path of file
count_tiles(path)

