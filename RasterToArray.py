#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 14:24:13 2020

@author: naomiberda
"""

import rasterio as rio
import numpy as np 

def transform(path,raster):
    """
    transform un raster de taille n*m*b (b=nombre de bandes)
    en un array de taille (n*m)*b (N*m colonnes, b lignes)
    """
    src=rio.open(path+raster)
    b=src.count #nombre de bandes
    (n,m)=src.shape #taille du raster
    matrice=np.zeros((n*m,b)) #taille de la matrice
    k=0 #nombre de pixels
    for i in range(n):
        for j in range(m):
            for bands in range(b):
                matrice[k,bands]=src.read(bands+1)[i,j]
                
        k+=1
   
    return(matrice)

def noNa(path,raster):
    """
    enleve les valeurs de nA
    Prend comme reference limage drone
    cree une liste de pixels nA (liste de liste)
    """
    src=rio.open(path+raster)
    
    
    
def write_csv(matrice,entetes):
    """
    ecrit un csv à partir dune matrice et dune entete (une liste de deux listes de taille de la matrice)
    """
    
    

    
if __name__=='__main__':
    path='/Volumes/My Passport 1/TempNaomi/Donnees/Planet/plot 2018/'
    raster='allindexesPlanet2018.tif'
    matrice=transform(path,raster)
    
    write_csv(matrice,entete)
    
    
