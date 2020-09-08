#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 21:54:48 2020

@author: naomiberda
"""


import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import r2_score, mean_squared_error

import matplotlib.pyplot as plt
#import scipy.stats
import csv
from os import listdir
import os

def regression_lineaire(X,Y):
    """
    input: X,Y, arrays
    output:a,b,R2 score,Ypred
    """
    lm=LinearRegression()
    reg=lm.fit(X,Y)
    a=reg.coef_[0]
    b=reg.intercept_
    Y_pred = lm.predict(X)
    r2=r2_score(Y,Y_pred)
    rmse=mean_squared_error(Y, Y_pred)
    moy=np.mean(Y)
    relat_rmse=rmse/moy
    return(a,b,r2,Y_pred,rmse,relat_rmse) 

def show_regression(X,Y,Xvalue,Yvalue):
    """
    Xvalue and Yvalue are the labels
    """
    (a,b,r2,Y_pred,rmse,relat_rmse)=regression_lineaire(X,Y)
    plt.scatter(Y_pred,Y)
    plt.plot(Y_pred,Y_pred,color='red')
    plt.title("r^2 = "+str(r2)[:5])
    plt.xlabel('Valeurs prédites avec l\'indice ' +str(Xvalue))
    plt.ylabel(Yvalue)
    plt.show()
 

  
def show_regression(X,Y,Xvalue,Yvalue):
    """
    Xvalue and Yvalue are the labels
    """
    (a,b,r2,Y_pred,rmse,relat_rmse)=regression_lineaire(X,Y)
    plt.scatter(Y_pred,Y)
    plt.plot(Y_pred,Y_pred,color='red')
    plt.title("r^2 = "+str(r2)[:5])
    plt.xlabel('Valeurs prédites avec l\'indice ' +str(Xvalue))
    plt.ylabel(Yvalue)
    plt.show()
    
    
class Data(object):
    
    def __init__(self,path2018,path2019):
        self.dataset_2018=pd.read_csv(path2018)
        self.dataset_2019=pd.read_csv(path2019)
        
    def reglin(self,Xvalue,Yvalue):
        """
        Xvalue and Yvalue are the label (str) of the values you want to do the reglin with, in the file you need
        """
        self.Y2018=np.array(self.dataset_2018[Yvalue])
        self.X2018=np.array(self.dataset_2018[Xvalue]).reshape(-1,1)
        (self.a18,self.b18,self.r218,self.Y_pred18,self.rmse18,self.relat_rmse18)=regression_lineaire(self.X2018,self.Y2018)

        self.Y2019=np.array(self.dataset_2019[Yvalue])
        self.X2019=np.array(self.dataset_2019[Xvalue]).reshape(-1,1)
        (self.a19,self.b19,self.r219,self.Y_pred19,self.rmse19,self.relat_rmse19)=regression_lineaire(self.X2019,self.Y2019)
   
    def showreg(self,Xvalue,Yvalue,annee):
       self.reglin(Xvalue,Yvalue)
       Y=self.Y2018
       X=self.X2018
       
       if annee=='2019':
          Y=self.Y2019
          X=self.X2019
          
       elif annee!='2018':
           print('erreur dans lannee, veuillez saisir 2018 ou 2019')
           
       show_regression(X,Y,Xvalue,Yvalue)
       
    def reglin_multiple(self,Xvalues,Yvalue,pathfinal):
        """
        Xvalues:list of labels
        Yvalue : str : Y label
        annee: year 2018 or 2019
        """
        Y2018=self.dataset_2018[Yvalue]
        X2018=self.dataset_2018[Xvalues]
        Y2019=self.dataset_2019[Yvalue]
        X2019=self.dataset_2019[Xvalues]
        
        lm2018=LinearRegression()
        reg2018=lm2018.fit(X2018,Y2018)
        a2018=reg2018.coef_
        b2018=reg2018.intercept_
        Y_pred2018=lm2018.predict(X2018)
        r218=reg2018.score(X2018,Y2018)
        rmse2018=mean_squared_error(Y2018, Y_pred2018)
        moy18=np.mean(Y2018)
        rrmse2018=rmse2018/moy18
          
        lm2019=LinearRegression()
        reg2019=lm2019.fit(X2019,Y2019)
        a2019=reg2019.coef_
        b2019=reg2019.intercept_
        Y_pred2019=lm2019.predict(X2019)
        r219=reg2019.score(X2019,Y2019)
        rmse2019=mean_squared_error(Y2019, Y_pred2019)
        moy19=np.mean(Y2019)
        rrmse2019=rmse2019/moy19
        
        
        nombre_indices=len(Xvalues)
        
        with open(pathfinal+'RegressionMultiples_modif.csv', 'w',newline='') as csvfile:
            fieldnames = ['coefficient','2018','2019']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for indices in range(nombre_indices):
                row={'coefficient':Xvalues[indices],'2018':str(round(a2018[indices],3)),'2019':str(round(a2019[indices],3))}
                writer.writerow(row)
            row1={'coefficient':'Terme constant','2018':str(round(b2018,2)),'2019':str(round(b2019,2))}
            row2={'coefficient':'r2','2018':str(round(r218,3)),'2019':str(round(r219,3))}
            row3={'coefficient':'Rrmse','2018':str(round(rrmse2018,3)),'2019':str(round(rrmse2019,3))}
            writer.writerow(row1)
            writer.writerow(row2)
            writer.writerow(row3)

       
    def write_csv_glob(self,Xvalues,Yvalue,pathfinal):
        """
        Xvalues : list of labels
        Yvalue:str: Y label
        """
        with open(pathfinal+'RegressionSimples.csv', 'w',newline='') as csvfile:
            fieldnames = ['indices','r2 2018','r2 2019','Rrmse 2018','Rrmse 2019','coeff dir 2018','coeff dir 2019']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for Xvalue in Xvalues:
                self.reglin(Xvalue,Yvalue)

                row={'indices':str(Xvalue),'r2 2018':str(round(self.r218,5)),'r2 2019':str(round(self.r219,5)),'Rrmse 2018':str(round(self.relat_rmse18,5)),'Rrmse 2019': str(round(self.relat_rmse19,5)),'coeff dir 2018':str(round(self.a18,2)),'coeff dir 2019':str(round(self.a19,2))}
               
                writer.writerow(row)
                
                
        
    
if __name__ == '__main__':
    path2018="/Volumes/My Passport 1/TempNaomi/Donnees/Planet/plot 2018/matrice_indices_20181004.csv"
    path2019="/Volumes/My Passport 1/TempNaomi/Donnees/Planet/plot 2019/matrice_indices_2019.csv"
    pathfinal="/Volumes/My Passport 1/TempNaomi/Donnees/Planet/"
    Xvalues= [' NDVI norm value',' GNDVI value',' MSVAI value']
    Yvalue='yield estimation value(kg.m-1)'
    Xvalue =' GNDVI value'
    A=Data(path2018,path2019)
    A.reglin_multiple(Xvalues,Yvalue,pathfinal)
    #A.write_csv_glob(Xvalues,Yvalue,pathfinal)
    #print(A.a19,A.b19)
    #A.showreg(Xvalue,Yvalue,'2019')
    
        

        