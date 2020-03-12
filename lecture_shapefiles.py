import geopandas as gpd
import matplotlib.pyplot as plt 
from descartes import PolygonPatch

"""
Before running the script, change the path and the files names, below
Put the files name in the list "Files"
"""


##fonctions

class Shapefile(object):
    
    def __init__(self,path,Files):
        self.path=path
        self.Files=Files
        
    def load_shapefile(self):
        """
        Creates a list of Geodataframes, corresponding to the shapefiles input
        
        """
        self.SHP=[] #creates the list of geodataframes
        for k in range (len(self.Files)):
            test=gpd.read_file(self.path+self.Files[k]) #creates a frame corresponding to a shapefile
            self.SHP+=[test] #adds the frame to the list

        
    def  change_projection(self,projection):
        """
        Puts all the shapefile in the projection wanted (4326)
        """
        self.load_shapefile() #loads the shapefiles and creates self.SHP
        idproj = projection[5:] #id of the projection_ Ex:4326
        for k in range(len(self.SHP)):
            file=self.SHP[k]
            newfile = file.to_crs(epsg=idproj)
            self.SHP[k]=newfile

    def plot_shapefiles(self):
        """
        Plot the shapefiles altogether
        """
        self.change_projection('epsg:4326') #we choose projection EPSG:4326
        colors=['#ffff00','#6699cc','#791cf8','#FF69B4','#00ff7f','#ff0000','#ff7f50']
        fig = plt.figure() 
        for j in range(len(self.Files)):
            self.test =  self.SHP[j]
            colorey=colors[j]
            #self.test.plot(color=colorey)
            
            
            for k in range(len(self.test.index)):
                i=int(self.test.index[k])
                
                poly= self.test['geometry'][i]
                ax = fig.gca() 
                ax.add_patch(PolygonPatch(poly, fc=colorey, ec=colorey, alpha=0.5, zorder=2 ))
                ax.axis('scaled')
        plt.show()
  
      
###CODE           
#2018 data           
#path = "/Users/naomiberda/Desktop/stage_3A/dataset/Shapefiles/2018/"
#Files= ["whole-plot.shp","Yield9Plots_4326.shp","Faidherbia.shp","Shelter.shp"]

#2019 data
path="/Users/naomiberda/Desktop/stage_3A/dataset/Shapefiles/2019/" #change the path to the file path of your computer
Files=["Plot.shp","Subplots.shp","faidherbias.shp","Others.shp"] #names of the shapefiles


A=Shapefile(path,Files)
A.plot_shapefiles()
