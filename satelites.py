#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 11:23:54 2020

@author: naomiberda
"""


import rasterio as rio
import numpy as np
from rasterio.plot import show
import os

def loadValueMask(path,raster,a,b):
    """
    path: path of the raster (str)
    raster : str : name of the raster (with one band, already masked)
    
    a,b :float : coefficients 
  
    """
    src=rio.open(path+raster)
    newr=src.read(1) #array
    newr=newr.astype(float)
    profile=src.profile
    profile.update(
           dtype=rio.float64,
           count=1,
           compress='lzw')
    newraster=np.zeros(newr.shape)
   
    newraster=a*newr+b
    
    show(newraster)
    
    newpath = path+'valuesModel/'
        
    if not os.path.exists(newpath):
                os.makedirs(newpath)
    with rio.open(newpath+raster[:-4]+'modelyield.tif', 'w', **profile) as dst:
                dst.write(newraster.astype(rio.float64), 1)
    
    


if __name__=='__main__':
     path="/Volumes/My Passport 1/TempNaomi/Donnees/Planet/plot 2018/NDVI_norm_0/"
     raster="Planet_2018_10_28_4326plot_NDVI_norm_0.tif"
     
     
     
     #2018
     a=484.37994044181033
     b=-148.84420526219887
     
     
     #sept 2019
     #a=260.749047942298
     #b=-17.5690341051343
     loadValueMask(path,raster,a,b)
     
    