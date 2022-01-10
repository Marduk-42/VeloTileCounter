# VeloTileCounter

To get the number of VeloViewer/Statshunters tiles that are within or border a specific country, follow these steps:

1.  Download border data from https://gadm.org/download_country.html as KMZ file
2.  Extract the file inside
3.  Set ```path``` to the path of the file
4.  Run

For larger countries / areas it might take some time!
You can use tqdm to get a rough estimate on the progess by importing [tqdm](https://github.com/tqdm/tqdm) and
using ```for tile in tqdm(tiles)``` instead of ```for tile in tiles``` in the ```count_tiles``` function.

### Requirements
* [shapely](https://github.com/shapely/shapely)
* [fastkml](https://github.com/cleder/fastkml)

[tqdm](https://github.com/tqdm/tqdm) is optional


### Counting tiles of subdivisions
To get the number of tiles within a subdivion, you can download the level-1, level-2, ... data from gadm and follow the same steps above.
The script will return the number of tiles for every subdivision.
You can also skip a subdivions or only include specific ones:
```count_tiles(path, names=['New York'])``` will count the number of tiles in the state of New York.
```count_tiles(path, skip_names=['Alaska', 'Texas'])``` will count the number of tiles in every state except Alaska and Texas.
(file needs to be the Level 1 USA kml file)
The names need to be the official names used by the corresponding country, not necessarily English!

### Tiles inside a country
To get the tiles inside a country (without the tiles that are only at the border), you can use the old ```_count_tiles``` function and  replace ```border.intersects``` with ```border.contains```.

### Example data
If not stated otherwise, islands (also small ones) are counted too.

| Area | Number of tiles |  Comment |
|---|---|---|
| Bavaria | 28169 | (part of Germany) |
| Belgium | 13255 |   |
| Czech Republic | 32272 | |
| Germany | 154563 | |
| Hungary | 34337 | |
| Luxembourg | 1145 |   |
| Netherlands | 17565 | Only European area |
| Poland | 139897 | |
| Switzerland | 15324 | |
| United Kingdom | 126543 | |

### How does it work?
1. The border data is extracted from the KML file
2. Starting at zoom level 1 (four tiles for about the entire world), a loop iterates through all tiles and calculate the area of the intersection between the tile and the country.
3.1 If the area of the intersection is equal to the area of the tile, the tile is inside the country, so the number of level 14 tiles within that tile are added
3.2 If the area of the intersection is not zero, but not equal either, the tile will be divided into four smaller tiles (if it has not reached the maximum zoom level yet), which will then be measured in the next loop.

### To-Do
* Uploading tile numbers for every territory
