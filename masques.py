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
#from os.path import isfile
import csv


class NDVI(object):
    """
    calculates the NDVI and loads NDVI images and normalized_NDVI images
    loads a CSV file with all the normalized NDVI data.
    NDVI=(NIR-Red)/(NIR+Red)
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
        np.seterr(divide='ignore', invalid='ignore')
        self.ndvi = np.zeros(red.shape)
        self.ndvi = (self.nir-self.red)/(self.nir+self.red)
        #show(self.ndvi)
        
    
    def load_NDVI(self,raster):
        """
        shows and loads the ndvi image in a 'ndvi' new directory
        """
        newpath = self.path+'ndvi/'
        
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            
        self.calculate_NDVI(raster)
        with rio.open(newpath+raster[:-4]+'_ndvi.tif', 'w', **self.profile) as dst:
            dst.write(self.ndvi.astype(rio.float64), 1)
        
        
        #show(self.ndvi)
        
    def calculate_normalized_NDVI (self,raster) :
        """
        calculates the normalized NDVI (not considering the soil)
        """
        self.calculate_NDVI(raster)
        self.ndvi_norm=self.ndvi[:] #copies the ndvi array
        (a,b)=np.shape(self.ndvi_norm)
        NDVI_sol=np.nanmin(self.ndvi_norm)
        NDVI_max=np.nanmax(self.ndvi_norm)
        NDVI_tot=0
        count=0
        for i in range(a):
            for j in range(b):
                item=self.ndvi_norm[i,j]
                if  np.isnan(item)==False:
                   self.ndvi_norm[i,j]=(item-NDVI_sol)/(NDVI_max-NDVI_sol)
                   NDVI_tot+=float(self.ndvi_norm[i,j])
                   count+=1 #on compte le nombre de pixel que l'on considere (pour faire la moyenne)
        
        self.NDVI_moyen=NDVI_tot/count
        self.NDVI_total=NDVI_tot
        #show(self.ndvi_norm)
        
    def load_normalized_NDVI(self,raster):
        """
        shows and loads the ndvi image in a 'ndvi' new directory
        """
        newpath = self.path+'normalized_ndvi/'
        
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            
        self.calculate_normalized_NDVI(raster)
        with rio.open(newpath+raster[:-4]+'_normalized_ndvi.tif', 'w', **self.profile) as dst:
            dst.write(self.ndvi_norm.astype(rio.float64), 1)
            
    def write_norm_NDVI(self):
        """
        input: the directory containing the raster files
        output : a csv file with the normalized ndvi values
        """
        with open(path+'NDVI.csv', 'w') as csvfile:
            fieldnames = ['file_name', 'NDVI_mean','NDVI_total']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
   
            for file in listdir(self.path):
                if '.tif' in file:
                    self.calculate_normalized_NDVI(file)
                    writer.writerow({'file_name':file , 'NDVI_mean':str(self.NDVI_moyen) ,'NDVI_total':str(self.NDVI_total)})

        
    def load_NDVI_dir(self):
        """
        loads all the ndvi images from a directory
        """
        for file in listdir(self.path):
            if '.tif' in file :
                self.load_NDVI(file)
    def load_norm_NDVI_dir(self):
        """
        loads all the normalized ndvi images from a directory
        """
        for file in listdir(self.path):
            if '.tif' in file :
                self.load_normalized_NDVI(file)
                
class EVI(object):
    """
    EVI=2,5((NIR-Red)/(NIR+6R-7,5B+1))
    """
    def __init__(self,path):
        self.path = path
    def calculate_EVI(self,raster):
        R=opr.Raster(self.path,raster)
        self.src=R.src
        red = self.src.read(4)
        self.red=red.astype(float)
        NIR = self.src.read(5)
        self.nir=NIR.astype(float)
        blue=self.src.read(1)
        self.blue=blue.astype(float)
        self.profile = self.src.profile
        self.profile.update(
            dtype=rio.float64,
            count=1,
            compress='lzw')
        np.seterr(divide='ignore', invalid='ignore')
        self.evi = np.zeros(red.shape)
        self.evi = 2.5*((self.nir-self.red)/(self.nir+6*self.red-7.5*self.blue+1))
        
        #show(self.evi)
        
    def EVI_threshold(self,raster,threshold):
        """
        thresold: un float compris entre 0 et 1.5 (le seuil)
        """

      
        self.calculate_EVI(raster)
        (a,b)=np.shape(self.evi)
        self.evi_tot=0
        self.evi_threshold=self.evi[:]
        for i in range(a):
            for j in range(b):
                item=self.evi[i,j]
                if item<=threshold:
                    self.evi_threshold[i,j]=0
                    self.evi_tot+=item
        show(self.evi_threshold)
      
        print(self.evi_tot)
                

    def load_EVI(self,raster):
        self.calculate_EVI(raster)
        newpath = self.path+'evi/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        with rio.open(newpath+raster[:-4]+'_evi.tif', 'w', **self.profile) as dst:
            dst.write(self.evi.astype(rio.float64), 1)
        show(self.evi)

        
    def load_EVI_dir(self):
        """
        loads all the ndvi images from a directory
        """
        for file in listdir(self.path):
            if '.tif' in file :
                self.load_EVI(file)
                
    def write_EVI(self):
        pass
    
                
    
if __name__=='__main__':
    path="/Volumes/My Passport/TempNaomi/Donnees/Drone/2018/Niakhar/2018_10_08/placettes2018/"
    raster="RS_multimosaic_2018_10_08_3_0.5R.tif"
    A=EVI(path)
   # B=NDVI(path)
    A.load_EVI_dir()
    #print(np.max(A.evi))
    #B.show_normalized_NDVI(raster)
    #A.write_norm_NDVI()
    #print(A.NDVI_moyen)