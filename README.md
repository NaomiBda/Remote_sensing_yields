# Remote sensing yields
These scripts aim at treating drone and satellite images to estimate the yield of cereal fields in agroforestry in Senegal. 

## Installation
Before running any script, install the following packages : 
* geopandas
* rasterio
* descartes


You may run this line on Anaconda prompt

```bash
conda install -c conda-forge geopandas rasterio descartes 
```

## Dataset
You need : 
* Rasters of the fields (Drone or satellite images) : 2 fields (2018 and 2019) .
* Shapefiles of the plots, the field, the trees
* Yield mesurements (dry material)


## Description of files

* reglin.py : Toutes les régressions linéaires qui concernent les drones. Relie les données d'indices avec les données de rendement mesurées. 
* reglinsat.py : Toutes les regressions (simples et multiples) concernant les satellites. Lis un fichier csv tout simple
* RastertoArray.py : transforme le raster à 6 bandes en un array, puis un fichier scv regroupant les valeurs d'indices pour chaques pixels.
* mergebands.py : permet de regrouper plusieurs raster à une bande en un raster en plusieurs bandes.
* indexes.py : à partir d'un raster multibandes (R,G,B et NIR au moins), calcule tous les indices, les regroupe dans un csv , génère des rasters filtrés
* calculate_yield.py : transforme un raster en sa modellisation
* clip_raster.py : découpe un raster suivant l'emprise d'un shapefile (polygone)
* cross_val.py : tentative de cross-validation
* lai.py : calculs sur le lai
* lecture_shapefiles.py: permet d'ouvrir des shapefiles et de les exploiter en python


