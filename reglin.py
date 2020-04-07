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
        self.Y=np.array(self.dataset[Yvalue])
        self.X=np.array(self.dataset[Xvalue]).reshape(-1,1)
        lm=LinearRegression()
        reg=lm.fit(self.X,self.Y)
        self.a=reg.coef_
        self.b=reg.intercept_
        self.Y_pred = lm.predict(self.X)
        self.r2=r2_score(self.Y,self.Y_pred)
        
        
    def show_reg(self,Xvalue,Yvalue):
        self.regression(Xvalue,Yvalue)
        plt.scatter(self.X,self.Y)
        plt.plot(self.X,self.Y_pred,color='red')
        plt.show()
        
        
        
    def regression_glob(self,Xvalue):
        """
        input= the X label
        Regression for all the labels of the csv file. 
        returns a dictionary with all the r2 values.
        returns a dict with all the coeff values
        """
        self.dict_r2={}
        self.dict_coeff={}

        for value in self.dataset:
       
            if value!='ID_Placette'and value!=Xvalue:
                
                self.regression(Xvalue,value)
                self.dict_r2[value]=self.r2
                self.dict_coeff[value]=[self.a[0],self.b]
                
    def optimal_value(self,Xvalue):
        """
        Xvalue=str:X label
        returns the value with the best r2_score
        """
        self.regression_glob(Xvalue)
        keys=list(self.dict_r2.keys())
        r2max=0
        value_max=keys[0]
        for value in keys:
            r2=self.dict_r2[value]
            if r2>r2max:
                r2max=r2
                value_max=value
                
        self.value_max=value_max
        self.coeff_max=self.dict_coeff[value_max]
        self.show_reg(Xvalue,value_max)

if __name__=='__main__':
    path="/Volumes/My Passport/TempNaomi/Donnees/Drone/2018/calculs_2018/calculs-Tableau 1.csv"
    Xvalue='LAI-mil'
    Yvalue='LAI_EVI seuil = 0.5'
    A=Datas(path)
    A.optimal_value(Xvalue)
    #print(A.dict_coeff)
    #print(A.dict_r2)
    print(A.value_max)
    print(A.coeff_max)
    #print(A.dict_r2)
    #print(A.coeff)