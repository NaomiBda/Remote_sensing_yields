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
    return(a,b,r2,Y_pred)  
  
def show_regression(X,Y):
    """
    """
    (a,b,r2,Y_pred)=regression_lineaire(X,Y)
    plt.scatter(X,Y)
    plt.plot(X,Y_pred,color='red')
    plt.show()

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
        (self.a,self.b,self.r2,self.Y_pred)=regression_lineaire(self.X,self.Y)
        # lm=LinearRegression()
        # reg=lm.fit(self.X,self.Y)
        # self.a=reg.coef_
        # self.b=reg.intercept_
        # self.Y_pred = lm.predict(self.X)
        # self.r2=r2_score(self.Y,self.Y_pred)
        

    def show_reg(self,Xvalue,Yvalue):
        
        self.regression(Xvalue,Yvalue)
        show_regression(self.X,self.Y)
        # plt.scatter(self.X,self.Y)
        # plt.plot(self.X,self.Y_pred,color='red')
        # y=self.X
        # plt.plot(self.X,y,color='green')
        # plt.show()
 
    def regression_glob(self,Xvalue,label_values):
        """
        input= the X label
        label_values : values you do not wish to take into consideration
        Regression for all the labels of the csv file. 
        returns a dictionary with all the r2 values.
        returns a dict with all the coeff values
        """
        self.dict_r2={}
        self.dict_coeff={}
        
        datas=[value for value in self.dataset if value not in label_values and value!=Xvalue]
        for value in datas:
            self.regression(Xvalue,value)
            self.dict_r2[value]=self.r2
            self.dict_coeff[value]=[self.a,self.b]
            
                
    def optimal_value(self,Xvalue,label_values):
        """
        Xvalue=str:X label
        returns the value with the best r2_score
        """
        self.regression_glob(Xvalue,label_values)
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
        self.r2_max=r2max
    
        
    def recalc_NDVI(self,Xvalue,label_values):
        """
        from literature, you find that :
            NDVImil=0,219*LAImil+0,160
        You want to adjust the NDVI with this and the optimal LAI calcluated:
            LAIcalc=a*LAImes+b
        You obtain:
            NDVIcalc=a*NDVImil+b/219+0,160*(1-a)
        You want :
            NDVImil=NDVIcalc/a-(b/219+0.16(1-a))/a
            
        """
        self.optimal_value(Xvalue,label_values)
       
        [a,b]=self.coeff_max
        a=float(a)
        b=float(b)
       
        self.a_NDVI=1/a
        self.b_NDVI=(-1/a)*((b/219)+0.160*(1-a))
        
        

def reg_NDVI(path_LAI,path_NDVI,Xvalue):
    """
    input: the csv file containing NDVI values
    """
    A=Datas(path_LAI)
    A.recalc_NDVI('LAI-mil',['ID_Placette'])
    
    Xvalue='MS_Graines_Placette_(g_m_2)'
    label_values=['file_name','MS_Pailles_Placette_(g_m_2)']
    B=Datas(path_NDVI)
    B.optimal_value(Xvalue,label_values)
   
    Y=B.dataset[B.value_max]

    Y_adj=A.a_NDVI*Y+A.b_NDVI
  
    X=np.array(B.dataset[Xvalue]).reshape(-1,1)
    
    show_regression(X,Y_adj)
    
    (a,b,r2,Y_pred)=regression_lineaire(X,Y_adj)
    print("La valeur de r2 pour la reg lin ajustée est {} \nCoefficient directeur={} \nOrdonnée à l'origine ={} \n\n".format(r2,a,b))
    print(B.value_max)
    show_regression(X,Y)
    (a,b,r2,Y_pred)=regression_lineaire(X,Y)
    print("La valeur de r2 pour la reg lin non ajustée est {} \nCoefficient directeur={} \nOrdonnée à l'origine ={}".format(r2,a,b))
    

if __name__=='__main__':
    
    path="/Volumes/My Passport/TempNaomi/Donnees/Drone/2018/calculs_2018/calculs-Tableau 1.csv"
 
    path_NDVI="/Volumes/My Passport/TempNaomi/Donnees/Drone/2018/Niakhar/2018_10_08/placettes2018/EVI_2018.csv"
    
    Xvalue_NDVI='MS_Graines_Placette_(g_m_2)'
    #A.optimal_value(Xvalue,label_values)
    #print(A.dict_coeff)
    reg_NDVI(path,path_NDVI,Xvalue_NDVI)
    
   