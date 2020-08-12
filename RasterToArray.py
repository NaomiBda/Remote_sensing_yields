#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 14:24:13 2020

@author: naomiberda
"""

import rasterio as rio
import numpy as np 

def noNa(path_drone):
    """
    enleve les valeurs de nA
    Prend comme reference limage drone
    cree une liste de pixels nA (liste de liste)
    path contient path+raster du drone
    """
    src=rio.open(path_drone)
    band1=src.read(1)
    listeNa=[]
    (n,m)=src.shape
    for i in range(n):
        for j in range(m):
            if band1[i,j]<0:
                listeNa+=[[i,j]]
    return(listeNa)
    

def transform(path,raster,path_drone):
    """
    transform un raster de taille n*m*b (b=nombre de bandes)
    en un array de taille (n*m)*b (N*m colonnes, b lignes)
    la premiere colonne est l id des pixels (i*j)
    """
    listeNa=noNa(path_drone)
    a=len(listeNa)
    src=rio.open(path+raster)
    b=src.count #nombre de bandes
    (n,m)=src.shape #taille du raster
    matrice=np.zeros((n*m-a,b+2)) #taille de la matrice
    k=0 #nombre de pixels
    for i in range(n):
        for j in range(m):
            if [i,j] not in listeNa:
                matrice[k,0]=i
                matrice[k,1]=j
            
                for bands in range(b):
                
                    matrice[k,bands+2]=src.read(bands+1)[i,j]
                
                
                k+=1
   
    return(matrice)


    
    
def write_csv(matrice,entetes):
    """
    ecrit un csv à partir dune matrice et dune entete (une liste de deux listes de taille de la matrice)
    """
    
    

    
if __name__=='__main__':
    path='/Volumes/My Passport 1/TempNaomi/Donnees/Planet/plot 2018/'
    path_drone='/Volumes/My Passport 1/TempNaomi/Donnees/Drone/2018/Niakhar/2018_10_08/plot 2018/NDVI_norm_0/valuesModel/2018reprojetedrone.tif'
    raster='allindexesPlanet2018.tif'
    matrice=transform(path,raster,path_drone)
    print(matrice)
    #write_csv(matrice,entete)
    
    
