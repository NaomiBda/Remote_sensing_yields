import geopandas as gpd

import matplotlib.pyplot as plt 
from descartes import PolygonPatch



##fonctions

class Shapefile(object):
    
    def __init__(self,path,Files):
        self.path=path
        self.Files=Files
        
    def load_shapefile(self):
        """
        crée une liste de geodataframes qui correspondent au shapefiles en entrée
        
        """
        self.SHP=[]
        for k in range (len(self.Files)):
            test=gpd.read_file(self.path+self.Files[k])
            self.SHP+=[test]

        
    def  change_projection(self,projection):
        """
        mets tous les shapefiles en projection 4326
        """
        self.load_shapefile()
        idproj = projection[5:] #id of the projection_ Ex:4326
        for k in range(len(self.SHP)):
            file=self.SHP[k]
            newfile = file.to_crs(epsg=idproj)
            self.SHP[k]=newfile

    def plot_shapefiles(self):
        """
        affiche la superposition des shapefiles
        """
        colors=['#ffff00','#6699cc','#791cf8','#FF69B4','#00ff7f','#ff0000','#ff7f50']
        fig = plt.figure() 
        self.change_projection('epsg:4326') #met tout sur la projection 4326
        for j in range(len(self.Files)):
            self.test =  self.SHP[j]
            color=colors[j]
            
            for k in range(len(self.test.index)):
                i=int(self.test.index[k])
                
                poly= self.test['geometry'][i]
                ax = fig.gca() 
                ax.add_patch(PolygonPatch(poly, fc=color, ec=color, alpha=0.5, zorder=2 ))
                ax.axis('scaled')
        plt.show()
        

        

###CODE           
#2018 data           
path = "/Users/naomiberda/Desktop/stage_3A/dataset/Shapefiles/2018/"
Files= ["whole-plot.shp","Yield9Plots_4326.shp","Faidherbia.shp","Shelter.shp",]

#2019 data
##pathFiles=["Plot.shp","Subplots.shp","faidherbias.shp","Others.shp"]


A=Shapefile(path,Files)
A.plot_shapefiles()



