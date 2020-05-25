
"""
Created on Mon May 18 17:53:07 2020

@author: naomiberda
"""


import indexes as idx
import pandas as pd



def calculate_index(path,raster, mask,threshold):
    """
    """
    A=idx.fonctions_masks(path)
    A.chose_mask(raster, mask)
    A.thresholded(raster,mask,threshold)
    return(A.value)

def calculate_yield(path,raster,mask,threshold,path_result_file,index):
    value= calculate_index(path,raster,mask,threshold)
    dataset_index=pd.read_csv(path_result_file)
    a=float(dataset_index['coeff a'][index])
    b=float(dataset_index['coeff b'][index])
    
    
    yieldvalue = a*value+b
    return(yieldvalue)

if __name__=='__main__':
    path="/Volumes/My Passport/TempNaomi/Donnees/Drone/2018/Niakhar/2018_10_08/plot 2018/"
    raster="RS_multimosaic_2018_10_08plot.tif"
    path_result_file = "/Volumes/My Passport/TempNaomi/Donnees/Drone/Global optimal indexes/septembre2019/Results MS_Pailles_Placette_(g_m_2).csv"
    mask='NDVI_norm'
    threshold=0
    index=2
    print(calculate_yield(path,raster,mask,threshold,path_result_file,index))
    
    
    