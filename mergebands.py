#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 18:31:39 2020

@author: naomiberda
"""


import rasterio as rio
from rasterio.merge import merge
import os

def fusionner(path,liste_raster):
    os.chdir(path)
    src_list=[]
    for raster in liste_raster:
        src=rio.open(path+raster)
        src_list+=[src]
    mosaic, out_trans = merge(src_list)
    # Copy the metadata
    out_meta = src.meta.copy()

# Update the metadata
    out_meta.update({"driver": "GTiff",
                 "height": mosaic.shape[1],
                 "width": mosaic.shape[2],
                 "transform": out_trans,
                 "crs": "+proj=utm +zone=35 +ellps=GRS80 +units=m +no_defs "
                 }
                )
    out_fp=path+"Planet.tif"
    with rio.open(out_fp, "w", **out_meta) as dest:
        dest.write(mosaic)

    




if __name__=="__main__":
    path="/Volumes/My Passport 1/TempNaomi/Donnees/Drone/2018/Niakhar/2018_10_08/plot 2018/NDVI_norm_0/valuesModel/"
    liste=["Planet2018b1.tif","Planet2018b2.tif","Planet2018b3.tif","Planet2018b4.tif"]
    fusionner(path,liste)
    