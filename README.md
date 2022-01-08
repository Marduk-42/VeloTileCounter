# VeloTileCounter

To get the number of VeloViewer/Statshunters tiles are within or border a specific country, follow these steps:

1.  Download border data from https://gadm.org/download_country.html as KMZ file
2.  Extract the file inside
3.  Set ```path``` to the path of the file
4.  Run

For larger countries / areas it might take some time!
You can use tqdm to get a rough estimate on the progess by importing [tqdm](https://github.com/tqdm/tqdm) and
using ```for element in tqdm(tiles)``` instead of ```for element in tiles``` in the ```count_tiles``` function.

### Requirements
* [shapely](https://github.com/shapely/shapely)
* [fastkml](https://github.com/cleder/fastkml)

[tqdm](https://github.com/tqdm/tqdm) is optional, but recommended


### Counting tiles of subdivisions
To get the number of tiles within a subdivion, you can download the level-1, level-2, ... data from gadm and follow the same steps above.
The script will return the number of tiles for every subdivision.

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

### To-Do
* Get number of tiles within an area (not bordering)
* Count a single subdivion instead of all
* Uploading tile numbers for every country
