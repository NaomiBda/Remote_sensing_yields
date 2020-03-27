#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 11:30:02 2020

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
import numpy as np
import os
from os import listdir
import csv


class Masks(object):
    """
    input : path of the raster
            raster file
    calculates the indexes and loads numpy arrays containing the masked images
    """
    def __init__(self,path,raster):
        
        self.path=path
        self.raster=raster
        
    def calculate_mask(self):
        """
        generates geodata frame of the raster and extract the bands. 
        """
        R=opr.Raster(self.path,self.raster)
        self.src=R.src
        red = self.src.read(4)
        NIR = self.src.read(5)
        blue=self.src.read(1)
        green=self.src.read(2)
        self.red=red.astype(float)
        self.nir=NIR.astype(float)
        self.blue=blue.astype(float)
        self.green=green.astype(float)
        
        self.profile = self.src.profile
        self.profile.update(
            dtype=rio.float64,
            count=1,
            compress='lzw')
  
    def calculate_NDVI(self):
        """
        
        returns self.ndvi : an array with all ndvi values
        NDVI=(nir-red)/(nir+red)

        """
        self.calculate_mask()
        np.seterr(divide='ignore', invalid='ignore')
        self.ndvi = np.zeros(self.red.shape)
        self.ndvi = (self.nir-self.red)/(self.nir+self.red)
        
    def calculate_norm_NDVI(self,threshold=0):
        """
        Calculates the normalized ndvi = ndvi_norm=(ndvi-ndvi_sol)/(ndvi_max-ndvi_sol)
        generates a ndvi_norm raster : (self.ndvi_norm)
        Calculates the mean of all normalized ndvi on the image : self.NDVI_moyen
        returns also the total of all ndvi_norm values = self.NDVI_tot

        """
        self.calculate_NDVI()
        self.ndvi_norm=self.ndvi[:] #copies the ndvi array
        (a,b)=np.shape(self.ndvi_norm)
        NDVI_sol=np.nanmin(self.ndvi_norm)
        NDVI_max=np.nanmax(self.ndvi_norm)
        self.NDVI_tot=0
        count=0
        for i in range(a):
            for j in range(b):
                item=self.ndvi[i,j]
                if np.isnan(item)==True or item<=threshold:
                    self.ndvi_norm[i,j]=0
                else:
                   self.ndvi_norm[i,j]=(item-NDVI_sol)/(NDVI_max-NDVI_sol)
                   self.NDVI_tot+=float(self.ndvi_norm[i,j])
                   count+=1 #on compte le nombre de pixel que l'on considere (pour faire la moyenne)
        try :
            self.NDVI_moyen=self.NDVI_tot/count
        except:
            self.NDVI_moyen=self.NDVI_tot
        
        
      

    def calculate_EVI(self,threshold=0):
        """
        Calculates the Enhanced Vegetation Index : 
            EVI=2.5*((nir-red)/(nir+6*red-7.5*blue+1))
        input: threshold : eliminate pixels with low EVI value (non vegetation). Default=0 (no threshold)
        returns:
            self.evi : array containing all evi values
            self.EVI_tot: Total Evi of the image (sum of all EVI)
            self.EVI_mean = mean of EVI of the image
            
        
        """
        self.calculate_mask()
        np.seterr(divide='ignore', invalid='ignore')
        self.evi = np.zeros(self.red.shape)
        self.evi = 2.5*((self.nir-self.red)/(self.nir+6*self.red-7.5*self.blue+1))
        
        (a,b)=np.shape(self.evi)
        self.EVI_tot=0
        self.evi_threshold=self.evi[:]
        count=0
        for i in range(a):
            for j in range(b):
                item=self.evi[i,j]
                if np.isnan(item)==True or item<=threshold:
                    self.evi_threshold[i,j]=0
                else:
                    self.EVI_tot+=item
                    count+=1
      
        try :
            self.EVI_mean=self.EVI_tot/count
        except:
            self.EVI_mean=self.EVI_tot
       
       
            
class fonctions_masks(object):
    """
    calculates indexes value and the apply fonctions:
        chose_mask : loads a raster corresponding to the index wanted
        show_mask : shows the raster
        load_raster : loads the masked raster in a directory
        load_file = Apply the mask to all the files in a directiory and loads it
        write_csv : write all the indexes values for all the files in a csv file
    """
    def __init__(self,path):
        
        self.path=path
        
        
    
    def chose_mask(self,raster,mask='NDVI',threshold=0):
        """
        
        """
        A=Masks(self.path,raster)
        if mask == 'NDVI':
            A.calculate_NDVI()
            self.newimage=A.ndvi
        elif mask =='NDVI_norm':
            A.calculate_norm_NDVI(threshold)
            self.value=A.NDVI_moyen
            self.value_tot= A.NDVI_tot
            self.newimage=A.ndvi_norm
        elif mask == 'EVI':
            A.calculate_EVI(threshold)
            self.newimage=A.evi_threshold
            self.value=A.EVI_mean
            self.value_tot=A.EVI_tot
        self.profile=A.profile
        
        
    def show_mask(self,raster,mask='NDVI',threshold=0):
        """

        """
        self.chose_mask(raster,mask,threshold)
        show(self.newimage)

    def load_raster(self,raster,mask='NDVI',threshold=0):
        """
    

        """
            
        try:
            self.chose_mask(raster,mask,threshold)
               
            newpath = self.path+str(mask)+'_'+str(threshold)+'/'
        
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            with rio.open(newpath+raster[:-4]+'_'+str(mask)+'_'+str(threshold)+'.tif', 'w', **self.profile) as dst:
                dst.write(self.newimage.astype(rio.float64), 1)
        except: 
            
            print('No valid mask : please type either NDVI,EVI or NDVI_norm')
            
    def load_files(self,mask='NDVI',threshold=0):
        """

        """
        for file in listdir(self.path):
            if '.tif' in file :
                self.load_raster(file,mask,threshold)
    def write_csv(self,mask='NDVI_norm'):
        """
        

        """
        if mask=='NDVI_norm':
            li=np.arange(2,10,2)/10
        elif mask =='EVI':
            li=np.arange(4,11,1)/10
        
        with open(path+str(mask)+'.csv', 'w',newline='') as csvfile:
            fieldnames = ['file_name', str(mask)+'_mean',str(mask)+'_total']+["seuil = "+str(threshold) for threshold in li]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for file in listdir(self.path):
                self.chose_mask(file,mask)
                if '.tif' in file:
                    #self.calculate_normalized_NDVI(file)
                    row={'file_name':file , str(mask)+'_mean':str(self.value),str(mask)+'_total':str(self.value_tot) }
                    
                    for threshold in li:
                        self.chose_mask(file,mask,threshold)
                        
                        row["seuil = "+str(threshold)]=str(self.value)
                        
                    writer.writerow(row)


if __name__=='__main__':
    path="/Volumes/My Passport/TempNaomi/Donnees/Drone/2019/Niakhar/19-09-05/placettes_2019/"
    raster="multimosaic_RC_19_09_05_M1B.tif"
    
    B=fonctions_masks(path)
    B.write_csv('EVI')
    
    
    