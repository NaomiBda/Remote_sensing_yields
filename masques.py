"""
Created on Fri Mar 20 10:01:52 2020

@author: naomiberda
Rappel des couches sur les données drones de 2019
- couche1: R450 : Bleu
 - couche2: R530  : Vert
- couche3: R570 : Jaune
- couche4: R675 : Rouge
- couche5: R730 : NIR
- couche6: R850 : RedEdge
- couche7: LWIR 
- couche8: Alpha
"""

import open_raster as opr
import rasterio as rio
from rasterio.plot import show
#import matplotlib.pyplot as plt
import numpy as np
#import subprocess
import os
from os import listdir
from os.path import isfile


class NDVI(object):
    """
    loads the NDVI image of each file in a directory
    """
    def __init__(self,path):
        """
        input: path where is located the raster images
        """
        self.path=path
        

    def calculate_NDVI(self,raster):
        """
        input: the original raster
        calculates the ndvi for each pixel
        """
        
        R=opr.Raster(self.path,raster)
        self.src=R.src
        red = self.src.read(4)
        self.red=red.astype(float)
        NIR = self.src.read(5)
        self.nir=NIR.astype(float)
        #self.ndvi=np.empty(self.src.shape,stype=rio.float32)
        #check = np.logical_or ( self.red > 0, self.nir > 0 )
        self.profile = self.src.profile
        self.profile.update(
            dtype=rio.float64,
            count=1,
            compress='lzw')
        self.ndvi = np.zeros(red.shape)
        self.ndvi = (self.nir-self.red)/(self.nir+self.red)
        #self.ndvi = np.where ( check,  (self.nir - self.red ) / ( self.nir + self.red ), -999 )
        
    def calculate_normalized_NDVI (self,raster) :
        """
        calculates the normalized NDVI (not considering the soil)
        """
        self.calculate_NDVI(raster)
        
        
  
    def show_NDVI(self,raster):
        """
        shows and loads the ndvi image in a 'ndvi' new directory
        """
        newpath = self.path+'ndvi/'
        
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            
        self.calculate_NDVI(raster)
        with rio.open(newpath+raster[:-4]+'_ndvi.tif', 'w', **self.profile) as dst:
            dst.write(self.ndvi.astype(rio.float64), 1)
        
        
        show(self.ndvi)
        
    def show_NDVI_dir(self):
        """
        loads all the ndvi images from a directory
        """
        for file in listdir(self.path):
            if '.tif' in file :
                self.show_NDVI(file)
                
    
        
        
if __name__=='__main__':
    path="/Volumes/My Passport/TempNaomi/Donnees/Drone/2019/Niakhar/19-10-17/placettesNIR_2019/"
    raster="RS_multimosaic_2018_10_08_3_0.5R.tif"
    A=NDVI(path)
    A.show_NDVI_dir()