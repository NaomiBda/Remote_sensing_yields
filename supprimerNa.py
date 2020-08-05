#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 14:48:37 2020

@author: naomiberda
"""

import rasterio as rio
import numpy as np



def supprNA(path,raster,valueseuil):
    """
    supprime les valeurs abeerantes sur les images satellites
    valueseuil = value seuil ou on applique plutot 0.
    path, raster = string  : adresse de l image
    """
    src=rio.open(path+raster)

    newimage = src #on cree l'image de la meme taille
    band1=newimage.read(1)
    band2=newimage.read(2)
    band3=newimage.read(3)
    band4=newimage.read(4)
    (hauteur,largeur)=band1.shape #taille de limage
    for i in range(hauteur):
        for j in range(largeur):
            if band1[i,j]<0:
                band1[i,j]=0
                band2[i,j]=0
                band3[i,j]=0
                band4[i,j]=0
    
                
                
            

    
    

if __name__=="__main__":
    
    ##2018
    path="/Volumes/My Passport 1/TempNaomi/Donnees/Drone/2018/Niakhar/2018_10_08/plot 2018/NDVI_norm_0/valuesModel/"
    raster=raster="Planet2018.tif"
    
    ##2019
    