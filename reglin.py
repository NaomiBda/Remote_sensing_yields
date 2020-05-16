#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 15:19:41 2020

@author: naomiberda
"""


import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
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
 
def regression_PLS(X,Y):
    """
    X: matrice des descripteurs (valeurs des indices)
    Y: variable attendue (rdt)

    """
    pls2=PLSRegression(n_components=2)
    pls2.fit(X, Y)
    Y_pred=pls2.predict(X)
    
  
def show_regression(X,Y,Xvalue,Yvalue):
    """
    Xvalue and Yvalue are the labels
    """
    (a,b,r2,Y_pred,rmse,relat_rmse)=regression_lineaire(X,Y)
    plt.scatter(Y_pred,Y)
    plt.plot(Y_pred,Y_pred,color='red')
    plt.title("r^2 = "+str(r2)[:5])
    plt.xlabel('Valurs prédites avec l\'indice ' +str(Xvalue))
    plt.ylabel(Yvalue)
    plt.show()
    
    
def fct_ransac(X,Y):
    
    lr = LinearRegression()
    lr.fit(X, Y)
    ransac = linear_model.RANSACRegressor(residual_threshold=0.2)
    ransac.fit(X, Y)
    inlier_mask = ransac.inlier_mask_
    outlier_mask = np.logical_not(inlier_mask)
    line_X = np.arange(X.min(), X.max())[:, np.newaxis]
    line_y = lr.predict(line_X)
    line_y_ransac = ransac.predict(line_X)
    print("Estimated coefficients (true, linear regression, RANSAC):")
    print( lr.coef_, ransac.estimator_.coef_)
    lw = 2
    plt.scatter(X[inlier_mask], Y[inlier_mask], color='yellowgreen', marker='.',
                label='Inliers')
    plt.scatter(X[outlier_mask], Y[outlier_mask], color='gold', marker='.',
                label='Outliers')
    plt.plot(line_X, line_y, color='navy', linewidth=lw, label='Linear regressor')
    plt.plot(line_X, line_y_ransac, color='cornflowerblue', linewidth=lw,
             label='RANSAC regressor')
    plt.legend(loc='upper right')
    plt.xlabel("Input")
    plt.ylabel("Response")
    plt.show()


class Datas(object):
    def __init__(self,path_index,file,path_terrain):
        """
        path = path where CSV files with indexes are located
        file=csv file used
        path_terrain= csv file with field datas
        """
        
        self.dataset_index=pd.read_csv(path_index+file)
        self.path_terrain=path_terrain
        self.dataset_terrain=pd.read_csv(path_terrain,sep=';')
        

    def regression(self,Xvalue,Yvalue):
        """
        input:
            value : str : header of the value you want

        """
        self.Y=np.array(self.dataset_terrain[Yvalue])
        self.X=np.array(self.dataset_index[Xvalue]).reshape(-1,1)
        (self.a,self.b,self.r2,self.Y_pred,self.rmse,self.relat_rmse)=regression_lineaire(self.X,self.Y)
        
    def indice_recolte(self,grain_label,leaf_label):
        """
        """
        grain=np.array(self.dataset_terrain[grain_label])
        feuille=np.array(self.dataset_terrain[leaf_label]).reshape(-1,1)
        self.liste_recolte = np.array([grain[k]/feuille[k] for k in range(len(grain))])
        self.index_crop=np.mean(self.liste_recolte)
        self.index_crop_inlier=np.mean(self.liste_recolte[:-1])
        #plt.boxplot(self.liste_recolte,labels=['indices de récolte'])
        #plt.savefig('/Volumes/My Passport/TempNaomi/Donnees/Terrain/2018/boxplot_indice_recolte_2018.png')
        #print(self.liste_recolte)
        #print(self.index_crop,self.index_crop_inlier)
        
    def plot_indice_recolte(self,grain_label,leaf_label):
        self.indice_recolte(grain_label, leaf_label)
        plt.boxplot(self.liste_recolte,labels=['indices de récolte'])

    def show_reg(self,Xvalue,Yvalue):
        
        self.regression(Xvalue,Yvalue)
        show_regression(self.X,self.Y,Xvalue,Yvalue)
        
        
        
    def outlirs(self,Xvalue,Yvalue):
        self.regression(Xvalue,Yvalue)
        fct_ransac(self.X, self.Y)
 
    def regression_glob(self,Yvalue,label_values):
        """
        input= the X label
        label_values : values you do not wish to take into consideration
        Regression for all the labels of the csv file. 
        returns a dictionary with all the r2 values.
        returns a dict with all the coeff values
        """
        self.dict={}
        self.dict_rmse={}
        self.dict_r2={}
        
        
        Values=[value for value in self.dataset_index if value not in label_values ]
        
        
        for value in Values:
            
            self.regression(value,Yvalue)
            self.dict[value]=[self.a,self.b]
            self.dict_rmse[value]=self.relat_rmse
            self.dict_r2[value]=self.r2

    def optimal_value(self,Yvalue,label_values):
        """
        Xvalue=str:X label
        returns the value with the best r2_score
        """
        self.regression_glob(Yvalue,label_values)
        keys=list(self.dict.keys())
   
       
        optimal_rmse=min(self.dict_rmse.values())
        optimal_r2=max(self.dict_r2.values())
        
     
        
        for cle in keys:
            if self.dict_rmse[cle]==optimal_rmse:
                value_max_rmse=cle
            if self.dict_r2[cle]==optimal_r2:
                value_max_r2=cle
                
        
  
        self.coeff_max=self.dict[value_max_rmse]
        self.r2_max=optimal_r2
        self.rmsemin =optimal_rmse
        self.value_max_r2=value_max_r2
        self.value_max_rmse=value_max_rmse

    def recalc_NDVI(self,Yvalue,label_values):
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
        self.optimal_value(Yvalue,label_values)
       
        [a,b]=self.coeff_max
        a=float(a)
        b=float(b)
       
        self.a_NDVI=1/a
        self.b_NDVI=(-1/a)*((b/219)+0.160*(1-a))
        
class Datas_glob(object):
    
    def __init__(self,path_indexes_2018,path_indexes_2019,path_terrain_2018,path_terrain_2019,files):
       
        self.path_terrain2018=path_terrain_2018
        self.path_terrain2019=path_terrain_2019
        self.path_indexes_2018=path_indexes_2018
        self.path_indexes_2019=path_indexes_2019
        self.files=files

    def write_csv_glob(self,path_final,Yvalue,label_values):
        newpath = path_final+'Global optimal indexes/'
        
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            
        with open(newpath+'Results '+Yvalue+'.csv', 'w',newline='') as csvfile:
            fieldnames = ['indices','year','Optimal threshold r2','Optimal threshold rmse','r2 optimal value','Rrmse optimal value','coeff a','coeff b']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for file in files:
                file_name=file+'.csv'
                
                Data2018=Datas(self.path_indexes_2018,file_name,self.path_terrain2018)
                
                Data2019=Datas(self.path_indexes_2019,file_name,self.path_terrain2019)
                Data2018.optimal_value(Yvalue, label_values)
                
                Data2019.optimal_value(Yvalue, label_values)
                
                
                row1={'indices':str(file),'year':'2018','Optimal threshold r2':str(Data2018.value_max_r2),'Optimal threshold rmse':str(Data2018.value_max_rmse) ,'r2 optimal value':str(Data2018.r2_max) ,'Rrmse optimal value':str(Data2018.rmsemin),'coeff a':str(Data2018.coeff_max[0]) ,'coeff b':str(Data2018.coeff_max[1]) }
               
                writer.writerow(row1)
                row2={'indices':str(file),'year':'2019','Optimal threshold r2':str(Data2019.value_max_r2),'Optimal threshold rmse':str(Data2019.value_max_rmse) ,'r2 optimal value':str(Data2019.r2_max) ,'Rrmse optimal value':str(Data2019.rmsemin),'coeff a':str(Data2019.coeff_max[0]) ,'coeff b':str(Data2019.coeff_max[1]) }
                
                writer.writerow(row2)
 

# def reg_NDVI(path_LAI,path_NDVI,Yvalue):
#     """
#     input: the csv file containing NDVI values
#     """
#     A=Datas(path_LAI)
#     A.recalc_NDVI('LAI-mil',['ID_Placette'])
    
#     Yvalue='MS_Graines_Placette_(g_m_2)'
#     label_values=['file_name','MS_Pailles_Placette_(g_m_2)']
#     B=Datas(path_NDVI)
#     B.optimal_value(Yvalue,label_values)
   
#     Y=B.dataset[B.value_max_rmse]

#     Y_adj=A.a_NDVI*Y+A.b_NDVI
  
#     X=np.array(B.dataset[Yvalue]).reshape(-1,1)
    
#     show_regression(X,Y_adj)
    
#     (a,b,r2,Y_pred,rmse)=regression_lineaire(X,Y_adj)
#     print("La valeur de r2 pour la reg lin ajustée est {} \nCoefficient directeur={} \nOrdonnée à l'origine ={} \n\n".format(r2,a,b))
#     print(B.value_max_rmse)
#     show_regression(X,Y)
#     (a,b,r2,Y_pred,rmse)=regression_lineaire(X,Y)
#     print("La valeur de r2 pour la reg lin non ajustée est {} \nCoefficient directeur={} \nOrdonnée à l'origine ={}".format(r2,a,b))
    


if __name__=='__main__':
    
    path_indexes_2018="/Volumes/My Passport/TempNaomi/Donnees/Drone/2018/Niakhar/2018_10_08/placettes2018/CSV_files/"
    path_indexes_2019="/Volumes/My Passport/TempNaomi/Donnees/Drone/2019/Niakhar/19-09-05/placettes_2019/CSV_files/"
    path_terrain_2018="/Volumes/My Passport/TempNaomi/Donnees/Terrain/2018/donnees_terrain.csv"
    path_terrain_2019="/Volumes/My Passport/TempNaomi/Donnees/Terrain/2019/donnees_terrain.csv"
    path_LAI_2018="/Volumes/My Passport/TempNaomi/Donnees/Drone/2018/Niakhar/2018_10_08/placettes2018/bash indices/"
    
    Yvalue='MS_Graines_Placette_(g_m_2)'
    Xvalue ='NDVI_norm_mean'
   
    files=['NDVI','NDVI_norm','EVI','GNDVI','EXG','MSAVI']
    file='NDVI_norm.csv'
    label_values=['file name']
   
    path_final='/Volumes/My Passport/TempNaomi/Donnees/Drone/'
    #B=Datas_glob(path_indexes_2018,path_indexes_2019,path_terrain_2018,path_terrain_2019,files)
    #B.write_csv_glob(path_final,Yvalues, label_values)
    A=Datas(path_indexes_2019, file, path_terrain_2019)
    #A.optimal_value(Yvalues,label_values)
    A.show_reg(Xvalue, Yvalue)
    #print(A.r2_max)
    

   