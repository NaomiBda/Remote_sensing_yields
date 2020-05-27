#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:12:01 2020

@author: naomiberda
"""
import os
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt
import lecture_shapefiles as lsh
from rasterio.mask import mask
import json
import clip_raster as cr


class Raster(object):
    def __init__(self,path,File):
        self.path=path
        self.File=File
        self.Dir=path+File
        self.src= rio.open(self.Dir)
        self.proj=self.src.crs
        
    def show_raster(self):
        nb_bands=self.src.count
        if nb_bands<=3:
            show(self.src )#affiche l'image en taille relle (prend beaucoup de place)
        else:
            array = self.src.read([4,2,1])
            #show(self.src.read())
            show(array)
            
    def get_profile(self):
        """
        prints the profile of the raster
        """
        print(self.src.profile)
        

    def get_shapefile(self,path_shapefile,f_shapefile):
        """
        creates a shapefile object using lecture_shapefiles
        input: one file
        """
        self.Sh=lsh.Shapefile(path_shapefile,f_shapefile)
        self.Sh.change_projection('epsg:4326')
        self.S=self.Sh.SHP[0] #S is the shapefile object in python
        
        
    def crop_raster_plot(self,path_shapefile,f_shapefile) :
        """
        crops the raster using the shapefile and plots the superposed polygon and raster
        """
        self.get_shapefile(path_shapefile,f_shapefile)
        fig=plt.figure()
        self.Sh.plot_shapefiles(fig)
        self.show_raster()
        pass
        
        
    def crop_raster(self,path_shapefile,f_shapefile,annee):
        """
        crops the raster with the shapefile input and creates new rasters, in a new directory
        """
        inShp=path_shapefile+f_shapefile
        cr.clip(inShp,self.path,self.File,annee)


if __name__=='__main__' :
    #path= "/Volumes/My Passport/TempNaomi/Donnees/Drone/2018/Niakhar/2018_10_08/"
    #File="RS_multimosaic_2018_10_08.tif"
    #path= "/Volumes/My Passport/TempNaomi/Donnees/Drone/2019/Niakhar/19-10-17/"
    #pathe="/Volumes/My Passport/TempNaomi/Donnees/Drone/2019/Niakhar/19-10-17/placettes_2019/"
    #File="2019_10_17.tif"
    #Filed="2019_10_17_M1B_normalized_ndvi.tif"
    path="/Volumes/My Passport/TempNaomi/Donnees/Drone/2019/Niakhar/19-10-17/placettes_copie2019/"
    raster="2019_10_17_3cm_M1B.tif"
    A=Raster(path,raster)
    #B=Raster(pathe,Filed)
   # path_sh="/Volumes/My Passport/TempNaomi/Donnees/Shapefiles/2019/"
   # A.crop_raster(path_sh,"sublots_cp.shp",'2019')
    
    A.show_raster()
    #B.show_raster()
