#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 14:24:13 2020

@author: naomiberda
"""

import rasterio as rio
import numpy as np 
import pandas as pd

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
                matrice[k,0]=int(i)
                matrice[k,1]=int(j)
            
                for bands in range(b):
                
                    matrice[k,bands+2]=src.read(bands+1)[i,j]
                
                
                k+=1
   
    return(matrice)


    
    
def write_csv(path,matrice,header,formt):
    """
    ecrit un csv à partir dune matrice et dune entete (une liste de deux listes de taille de la matrice)
    path = path where to load the file
    matrice : array 
    header = str : header
    formt : format (int, float etc.. )
    """
    
    np.savetxt(path+"matrice_indices.csv", matrice, delimiter=",",fmt=formt,header=header)
    

    
if __name__=='__main__':
    #2018
   # path='/Volumes/My Passport 1/TempNaomi/Donnees/Planet/plot 2018/'
    #path_drone='/Volumes/My Passport 1/TempNaomi/Donnees/Drone/2018/Niakhar/2018_10_08/plot 2018/NDVI_norm_0/valuesModel/2018reprojetedrone.tif'
    #raster='allindexesPlanet2018.tif'
    
    #2019
    path='/Volumes/My Passport 1/TempNaomi/Donnees/Planet/plot 2019/'
    path_drone='/Volumes/My Passport 1/TempNaomi/Donnees/Drone/2019/Niakhar/19-09-05/plot 2019/NDVI_norm_0/valuesModel/drone2019projete.tif'
    raster='Planetallindexes2019.tif'
    
    
    #code
    matrice=transform(path,raster,path_drone)
    header='pixel line index,pixel column index,NDVI value, NDVI norm value,EVI value, GNDVI value,Excess green value, MSVAI value'
    formt='%d','%d','%1.4f','%1.4f','%1.4f','%1.4f','%d','%1.4f' # '%d' means only integeer values , '%1.4f' means decimal with 4 figures
    print(matrice)
    write_csv(path,matrice,header,formt)
    #write_csv(matrice,entete)
    
    
