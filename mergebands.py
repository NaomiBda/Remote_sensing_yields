#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 18:31:39 2020

@author: naomiberda
"""


import rasterio as rio


def fusionner (liste,path):

    # Read metadata of first file
    with rio.open(path+liste[0]) as src0:
        meta = src0.meta
    
    # Update meta to reflect the number of layers
    meta.update(count = len(liste))
    
    # Read each layer and write it to stack
    with rio.open(path+'stack.tif', 'w', **meta) as dst:
        for id, layer in enumerate(liste, start=1):
            with rio.open(path+layer) as src1:
                dst.write_band(id, src1.read(1))




if __name__=="__main__":
    #2018
    # path="/Volumes/My Passport 1/TempNaomi/Donnees/Drone/2018/Niakhar/2018_10_08/plot 2018/NDVI_norm_0/valuesModel/"
    # liste=["Planet2018b1.tif","Planet2018b2.tif","Planet2018b3.tif","Planet2018b4.tif"]
    # fusionner(liste,path)
    
    #2019
    path="/Volumes/My Passport 1/TempNaomi/Donnees/Drone/2019/Niakhar/19-09-05/plot 2019/NDVI_norm_0/valuesModel/"
    liste=["planetaligneb1.tif","planetaligneb2.tif","planetaligneb3.tif","planetaligneb1.tif"]
    fusionner(liste,path)
    
    
    
    