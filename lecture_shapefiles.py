#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 08:49:56 2020

@author: naomiberda
"""

import geopandas as gpd
#from geopandas import GeoDataFrame
import matplotlib.pyplot as plt 
from descartes import PolygonPatch
#from projection_shapefiles import change_projection


##fonctions

class Shapefile(object):
    
    def __init__(self,path,Files):
        self.path=path
        self.Files=Files
        
        
    def  change_projection(self,File,projection):
        """
        mets tous les shapefiles en projection 4326
        """
        file = gpd.read_file(self.path+File)
        dico = file.crs
        proj = dico['init']
        if proj == projection:
        #if the shapefile has a correct projection, it remains the same
            newfile=file
        else:
            idproj = projection[5:] #id of the projection_ Ex:4326
            orig = file.copy()
            newfile = file.to_crs(epsg=idproj)
        return(newfile)
        
        
    
    def affiche_shapefiles(self):
        """
        affiche la superposition des shapefiles
        """
        colors=['#ffff00','#6699cc','#791cf8','#FF69B4','#00ff7f','#ff0000','#ff7f50']
        fig = plt.figure() 
        for j in range(len(self.Files)):
            formes=self.Files[j]
            self.test = self.change_projection(formes,'epsg:4326') #met tout sur la projection 4326
            #self.test = GeoDataFrame.from_file(self.path+formes)
            #print(self.test['geometry'])
            #bounds = self.test.bounds
            #print(self.test.crs)
            color=colors[j]
            print(self.test.bounds)
            for k in range(len(self.test.index)):
                i=int(self.test.index[k])
                
                poly= self.test['geometry'][i]
                ax = fig.gca() 
                ax.add_patch(PolygonPatch(poly, fc=color, ec=color, alpha=0.5, zorder=2 ))
                ax.axis('scaled')
        
            plt.show()
        

    def extraire_images(self,image):
        pass
        

###CODE           
#2018 data           
path = "/Users/naomiberda/Desktop/stage_3A/dataset/Shapefiles/2018/"
Files= ["whole-plot.shp","Yield9Plots_4326.shp","Faidherbia.shp","Shelter.shp",]

#2019 data
path = "/Users/naomiberda/Desktop/stage_3A/dataset/Shapefiles/2019/"
Files=["Plot.shp","Subplots.shp","faidherbias.shp","Others.shp"]


A=Shapefile(path,Files)
A.affiche_shapefiles()


