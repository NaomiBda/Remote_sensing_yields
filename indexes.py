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
import matplotlib.pyplot as plt
from pylab import sqrt
import gdal


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
        
        
    def calculate_norm_NDVI(self):
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
        
        for i in range(a):
            for j in range(b):
                item=self.ndvi[i,j]
                
                if np.isnan(item)==False:
                   self.ndvi_norm[i,j]=(item-NDVI_sol)/(NDVI_max-NDVI_sol)

            
            
    def calculate_GNDVI(self):
        """
        returns self.gndvi: array containing  the gndvi index : 
            GNDVI=(nir-green)/(nir+green)
        input:
            threshold: float (O to 1)
            

        """
        self.calculate_mask()
        np.seterr(divide='ignore', invalid='ignore')
        self.gndvi = np.zeros(self.red.shape)
        self.gndvi = (self.nir-self.green)/(self.nir+self.green)
       

    def calculate_EVI(self):
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
       
            
    def calculate_excessgreen(self):
        """
        Exg= 2G-R-B
        """
        self.calculate_mask()
        np.seterr(divide='ignore', invalid='ignore')
        self.Exg= np.zeros(self.red.shape)
        self.Exg=2*self.green-self.red-self.blue
        
    def calculate_MSAVI(self):
        """
        MSAVI=(2*NIR+1-sqrt((2*NIR+1)^2-8*(NIR+RED)))/2

        """
        self.calculate_mask()
        np.seterr(divide='ignore', invalid='ignore')
        self.msavi=np.zeros(self.red.shape)
        self.msavi=(2*self.nir+1-sqrt((2*self.nir+1)**2-8*(self.nir-self.red)))/2
        
  
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
        
    def chose_mask(self,raster,mask):
        """
        CHOSES THE MASK, using the class 'mask'
        """
        A=Masks(self.path,raster)
        if mask=='NDVI':
            A.calculate_NDVI()
            self.newimage=A.ndvi[:]
            #self.value_min=-1
        elif mask=='EXG':
            A.calculate_excessgreen()
            self.newimage=A.Exg[:]
            #self.value_min=-1
        elif mask=='NDVI_norm':
            A.calculate_norm_NDVI()
            self.newimage=A.ndvi_norm[:]
            #self.value_min=0
        elif mask =='EVI':
            A.calculate_EVI()
            self.newimage=A.evi[:]
            #self.value_min=0
        elif mask =='GNDVI':
            A.calculate_GNDVI()
            self.newimage=A.gndvi[:]
            #self.value_min=-1
        elif mask=='MSAVI':
            A.calculate_MSAVI()
            self.newimage=A.msavi
            #self.value_min=-1
        self.value_min=np.nanmin(self.newimage)
        self.profile=A.profile
           
    def thresholded(self,raster,mask,threshold=-1):
        """
        
        apply a shreshold on a mask
        input: 'NDVI','norm_NDVI','EVI','GNDVI','EXG','MSAVI'
        self.chose_mask(raster,mask,threshold)
        """
        self.chose_mask(raster, mask)
        (a,b)=np.shape(self.newimage)
        
        #threshold=self.value_min
        self.value_tot=0
        count=0
        for i in range(a):
            for j in range(b):
                item=self.newimage[i,j]
                if np.isnan(item)==True or item<=threshold:
                    self.newimage[i,j]=self.value_min
                else:
                    count+=1
                    self.value_tot+=item
        try:
            self.value=self.value_tot/count
        except:
            self.value=self.value_tot

    def calculate_LAI(self,raster,mask='NDVI',threshold=-1):
        """
        mask : str : 'NDVI','EVI','GNDVI' etc
        calculates the leaf area index using indexes and thresholds
        """
        self.chose_mask(raster,mask)
        #show(self.newimage)
        (a,b)=np.shape(self.newimage)
        
        
        pixels_tot=0
        pixels_LAI=0
        self.lai=self.newimage[:]
        for i in range(a):
            for j in range(b):
                item=self.newimage[i,j]
                if np.isnan(item)==True :
                    self.lai[i,j]=self.value_min
                else:
                    pixels_tot+=1
                    if item>=threshold:
                        pixels_LAI+=1
                        self.lai[i,j]=1
                    else:
                        self.lai[i,j]=self.value_min
        try:
            self.LAI=pixels_LAI/pixels_tot
        except:
            self.LAI=pixels_LAI
        self.value=self.LAI
        self.newimage=self.lai
    
    def show_mask(self,raster,mask='NDVI',threshold=-1,mask_LAI='NDVI'):
        """
        display the mask
        input:
            raster: raster image
            mask:mask chosen (str ='NDVI,'EVI','NDVI_norm','GNDVI','LAI')
            threshold: threshold chosen (float)
            mask_LAI(optional) : if LAI chosen, mask ot apply the LAI on (default is NDVI)

        """
        if mask=='LAI':
            self.calculate_LAI(raster,mask_LAI,threshold)
        else:
            self.thresholded(raster,mask,threshold)
            
        show(self.newimage)

    def load_raster(self,raster,mask='NDVI',threshold=0):
        """
        input:
            raster adress
            mask : str : 'NDVI','NDVI_norm' or EVI 
            threshold: float: (default is O)
        Output: 
            creates a directory and load the new masked raster

        """
            
        try:
            self.thresholded(raster,mask,threshold)
               
            newpath = self.path+str(mask)+'_'+str(threshold)+'/'
        
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            with rio.open(newpath+raster[:-4]+'_'+str(mask)+'_'+str(threshold)+'.tif', 'w', **self.profile) as dst:
                dst.write(self.newimage.astype(rio.float64), 1)
        except: 
            
            print('No valid mask : please type either NDVI,EVI or NDVI_norm')
            
    def load_files(self,mask='NDVI',threshold=0):
        """
        loads all the file masked in a directory

        """
        for file in listdir(self.path):
            if '.tif' in file :
                self.load_raster(file,mask,threshold)
                
    def histo_values(self,raster,mask='NDVI'):
        """
        loads an histogram with all the values of indices for the pixels

        """
        self.thresholded(raster,mask)
        
        list_pixel=[]
        (a,b)=np.shape(self.newimage)
        for i in range (a):
            for j in range(b):
                list_pixel+=[self.newimage[i,j]]
         
        plt.hist(list_pixel)
        
 
        
    def write_csv(self,mask='NDVI_norm'):
        """
        input:
            mask : str :'NDVI_norm' or 'EVI' or'GNDVI'
        Output: a CSV file countaning the index values for all the thresholds 

        """
        if mask=='NDVI_norm':
            li=np.arange(2,10,2)/10
            
        elif mask =='EVI':
            li=np.arange(4,11,1)/10
        elif mask=='GNDVI':
            li=np.arange(30,55,5)/100
        elif mask=='NDVI':
            li=np.arange(0,10,2)/10
        elif mask =='EXG':
            li=np.arange(0,10,2)/10
        elif mask=='MSAVI':
            li=np.arange(2,10,2)/10

                    
        with open(path+str(mask)+'.csv', 'w',newline='') as csvfile:
            fieldnames = ['file_name', str(mask)+'_mean',str(mask)+'_total']+["seuil = "+str(threshold) for threshold in li]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for file in listdir(self.path):
                self.thresholded(file,mask)
                if '.tif' in file:
                    #self.calculate_normalized_NDVI(file)
                    row={'file_name':file , str(mask)+'_mean':str(self.value),str(mask)+'_total':str(self.value_tot) }
                    
                    for threshold in li:
                        self.thresholded(file,mask,threshold)
                        
                        row["seuil = "+str(threshold)]=str(self.value)
                        
                    writer.writerow(row)
                    
    def write_csv_glob(self):
        
        list_masks=['NDVI_norm','EVI','NDVI','GNDVI','EXG','MSAVI']
        list_li=[np.arange(2,10,2)/10,np.arange(4,11,1)/10,np.arange(0,10,2)/10,np.arange(30,55,5)/100,np.arange(0,10,2)/10,np.arange(2,10,2)/10]
        
        newpath = self.path+'CSV_files/'
        
        if not os.path.exists(newpath):
            os.makedirs(newpath)
           
        for k in range(len(list_masks)):
            mask=list_masks[k]
            li=list_li[k]
            with open(newpath+str(mask)+'.csv', 'w',newline='') as csvfile:
                fieldnames = ['File name', str(mask)+' mean',str(mask)+' total']+["seuil = "+str(threshold) for threshold in li]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
    
                for file in listdir(self.path):
                    self.thresholded(file,mask)
                    if '.tif' in file: 
                        #self.calculate_normalized_NDVI(file)
                        row={'File name':file , str(mask)+' mean':str(self.value),str(mask)+' total':str(self.value_tot) }
                        
                        for threshold in li:
                            self.thresholded(file,mask,threshold)
                            
                            row["seuil = "+str(threshold)]=str(self.value)
                            
                        writer.writerow(row)


if __name__=='__main__':
    path="/Volumes/My Passport/TempNaomi/Donnees/Drone/2019/Niakhar/19-09-05/placettes_2019/"
    raster="multimosaic_RC_19_09_05_M1B.tif"
    B=fonctions_masks(path)
    B.write_csv('NDVI_norm')
    #show(B.newimage)
    #B.thresholded(raster,'MSAVI',0)
    #B.show_mask(raster,'MSAVI',-1)
    #print(B.value_min)
    