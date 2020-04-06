#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 15:19:41 2020

@author: naomiberda
"""


import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

class Datas(object):
    def __init__(self,path):
        self.path=path
        self.dataset=pd.read_csv(path,sep=';',header=0)
        
    def regression(self,Xvalue,Yvalue):
        """
        input:
            value : str : header of the value you want

        """
        Y=np.array(self.dataset[Yvalue])
        X=np.array(self.dataset[Xvalue]).reshape(-1,1)
        lm=LinearRegression()
        reg=lm.fit(X,Y)
        self.coeff=reg.coef_
        Y_pred = lm.predict(X)
        self.r2=r2_score(Y,Y_pred)
        plt.scatter(X, Y)
        plt.plot(X, Y_pred, color='red')
        plt.show()
        
    def regression_glob(self):
        self.dict_r2={}
        for value in self.dataset:
            
            if value=='LAI-mil':
                Xvalue=self.dataset[value]
                
            elif value!='ID_Placette':
                Yvalue=self.dataset[value]
                #print(Yvalue)
                self.regression(Xvalue,Yvalue)
                self.dict_r2[value]=self.r2
        

if __name__=='__main__':
    path="/Volumes/My Passport/TempNaomi/Donnees/Drone/2018/calculs_2018/calculs-Tableau 1.csv"
    Xvalue='LAI-mil'
    Yvalue='LAI_EVI seuil = 0.5'
    A=Datas(path)
    A.regression_glob()
    #print(A.dict_r2)
    #print(A.coeff)