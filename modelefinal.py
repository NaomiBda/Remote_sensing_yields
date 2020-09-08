#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 00:15:18 2020

@author: naomiberda
"""

import rasterio as rio
import indexes as ix
import pandas as pd
import numpy as np
import os

##calculate indexes

def load_indexes(path,raster,list_indexes):
    """
    loads indexes that you need for modelling 
    list_indexes : list of indexes you need
    """
    A=ix.fonctions_masks(path)
    for index in list_indexes:
        A.load_raster(raster,index,-2,'satellite')
        
        
def load_yield(path,raster_list,coeff_list):
    """
    raster_list : list of str : rasters
    coeff_list : coeff to adjust with rasters (same lenght+1 (last value is b), same rank )
    """
    src=rio.open(path+raster_list[0])
    profile=src.profile
    profile.update(
           dtype=rio.float64,
           count=1,
           compress='lzw')
    band=src.read(1)
    newraster=np.zeros(band.shape)
    
    
    for k in range(len(raster_list)):
        src=rio.open(path+raster_list[k])
        band=src.read(1)
        band=band.astype(float)
        newraster+=band*coeff_list[k]
    newraster+=coeff_list[k]
    
    newpath = path+'valuesModel/'
    if not os.path.exists(newpath):
                os.makedirs(newpath)
    with rio.open(newpath+raster_list[0][:-14]+'modelyield.tif', 'w', **profile) as dst:
                dst.write(newraster.astype(rio.float64), 1)
    
     
    
if __name__=='__main__':
    path18="/Volumes/My Passport 1/TempNaomi/Donnees/Planet/Planet2018indices/"
    path19="/Volumes/My Passport 1/TempNaomi/Donnees/Planet/Planet2019indices/"
    
    raster18="Planet_2018_10_04_4326.tif"
    raster_list18=['Planet_2018_10_04_4326_NDVI_norm.tif','Planet_2018_10_04_4326_GNDVI.tif','Planet_2018_10_04_4326_MSAVI.tif']
    coeff18=[-701.446,152.958,3883,452,-1749,94]
    raster19="Planet_2019_09_12_4326.tif"
    coeff19=[515.089,420.203,1542.337,327.64]
    raster_list19=['Planet_2019_09_12_4326_NDVI_norm.tif','Planet_2019_09_12_4326_GNDVI.tif','Planet_2019_09_12_4326_MSAVI.tif']
    
    list_indexes=['NDVI_norm','GNDVI','MSAVI']
    #load_indexes(path,raster19,list_indexes)
    load_yield(path18,raster_list18,coeff18)
    #load_yield(path19,raster_list19,coeff19)
    


