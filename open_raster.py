#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:12:01 2020

@author: naomiberda
"""
import os
import rasterio as rio
from rasterio.plot import show
import matplotlib 
import matplotlib.pyplot as plt
import lecture_shapefiles as lsh
from descartes import PolygonPatch


class Raster(object):
    def __init__(self,path,File):
        self.path=path
        self.File=File
        self.Dir=path+File
        self.src= rio.open(self.Dir)
        self.proj=self.src.crs
        
    def show_raster(self):
        show(self.src )#affiche l'image en taille relle (prend beaucoup de place)
        
    def match_projection(self,projection):
        projection=self.proj
        pass
        
        
    def get_shapefile(self,path_shapefile,f_shapefile):
        """
        creates a shapefile object using lecture_shapefiles
        input: one file
        """
        
        Sh=lsh.Shapefile(path_shapefile,f_shapefile)
        Sh.change_projection('epsg:4326')
        self.S=Sh.SHP[0] #S is the shapefile object in python
        
        
    def crop_raster_plot(self,path_shapefile,f_shapefile) :
        """
        crops the raster using the shapefile and plots the superposed polygon and raster
        """
        self.get_shapefile(path_shapefile,f_shapefile)
        
        features = [feature for feature in self.S['geometry']]
        show(self.src)
        ax = plt.gca()
        
        patches = [PolygonPatch(feature,edgecolor="red",facecolor="none", linewidth=2) for feature in features]
        ax.add_collection(matplotlib.collections.PatchCollection(patches))
        
    def crop_raster(self,path_shapefile,f_shapefile):
        """
        crops the raster with the shapefile input and creates nex rasters, in a new directory
t        """
        self.get_shapefile(path_shapefile,f_shapefile)
        currentDir=self.path
        newpath = currentDir+'/cropped_'+f_shapefile[:-4]
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        

path= "/Volumes/My Passport/TempNaomi/Donnees/Drone/2019/Niakhar/19-09-05/"
File="multimosaic_RC_19_09_05.tif"

A=Raster(path,File)

path_sh="/Users/naomiberda/Desktop/stage_3A/dataset/Shapefiles/2019/"
#A.crop_raster_plot(path_sh,"Subplots.shp")
A.show_raster()


