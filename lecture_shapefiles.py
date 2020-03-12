import geopandas as gpd

import matplotlib.pyplot as plt 
from descartes import PolygonPatch



##fonctions

class Shapefile(object):
    
    def __init__(self,path,Files):
        self.path=path
        self.Files=Files
        
        
    def  change_projection(self,File,projection):
        """
        mets tous les shapefiles en projection 4326
        """
        file = gpd.read_file(self.path+File)
        idproj = projection[5:] #id of the projection_ Ex:4326
        newfile = file.to_crs(epsg=idproj)
        return(newfile)

    def affiche_shapefiles(self):
        """
        affiche la superposition des shapefiles
        """
        colors=['#ffff00','#6699cc','#791cf8','#FF69B4','#00ff7f','#ff0000','#ff7f50']
        fig = plt.figure() 
        for j in range(len(self.Files)):
            formes=self.Files[j]
            self.test = self.change_projection(formes,'epsg:4326') #met tout sur la projection 4326
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
A.affiche_shapefiles()


