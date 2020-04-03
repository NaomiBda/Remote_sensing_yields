"""
Created on Mon Mar 30 09:28:48 2020

@author: naomiberda
"""
import numpy as np
import indexes as ix
from rasterio.plot import show
import csv
from os import listdir

class LAI(object):
    def __init__(self,path):
        self.path=path
    def calculate_LAI(self,raster,threshold=-1):
        """
       
        """
        Image=ix.Masks(self.path,raster)
        Image.calculate_NDVI()
        (a,b)=np.shape(Image.ndvi)
        pixels_tot=0 #total number of pixels in the image
        pixels_LAI=0 #number of pixels over the threshold
        self.lai=Image.ndvi[:]
        for i in range(a):
            for j in range(b):
                item=Image.ndvi[i,j]
                if np.isnan(item) :
                    self.lai[i,j]=-1
                else:
                    pixels_tot+=1
                    if item<=threshold:
                        self.lai[i,j]=-1
                    else:
                        pixels_LAI+=1
                        self.lai[i,j]=1
   
        self.LAI=pixels_LAI/pixels_tot
        

        
    def show_LAI(self,raster,threshold):
        """
        """
        self.calculate_LAI(raster,threshold)
        show(self.lai)
        
    def write_LAI(self):
         with open(self.path+'LAI.csv', 'w',newline='') as csvfile:
            fieldnames = ['file_name']+["seuil = "+str(threshold) for threshold in np.arange(0,8)/10]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for file in listdir(self.path):
                
                if '.tif' in file:
                    #self.calculate_normalized_NDVI(file)
                    row={'file_name':file }
                    
                    for threshold in np.arange(0,8)/10:
                        self.calculate_LAI(file,threshold)

                        row["seuil = "+str(threshold)]=str(self.LAI)
                        
                    writer.writerow(row)
        

        
if __name__=="__main__":
    path="/Volumes/My Passport/TempNaomi/Donnees/Drone/2018/Niakhar/2018_10_08/placettes2018/"
    raster="multimosaic_RC_19_09_05_M1B.tif"
    A=LAI(path)
    A.write_LAI()
    #A.show_LAI(raster,0.5)
    #print(A.LAI)
    
