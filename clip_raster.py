import geopandas 
import rasterio
from rasterio.mask import mask
import json
import os

def clip (inShp,path_raster, inRaster):
    newpath = path_raster+'plot/'
        
    if not os.path.exists(newpath):
            os.makedirs(newpath)
            
    df = geopandas.read_file(inShp)
    with rasterio.open(path_raster+inRaster) as ds:
        profile = ds.profile
        for index, row in df.iterrows():
            coords = [json.loads(df.to_json())['features'][index]['geometry']]
            masked, out_transform = mask(dataset=ds, shapes=coords, crop=True)
            profile.update(transform=out_transform,height=masked.shape[1],width=masked.shape[2])
            
            outName = inRaster.replace('.tif','plot.tif')
            with rasterio.open(newpath+outName,'w',**profile) as outds :
                for i in range (ds.count):
                    outds.write(masked[i,:,:],i+1)
                    
if __name__=='__main__' :
    #inShp = "/Volumes/My Passport/TempNaomi/Donnees/Shapefiles/2018/Yield9Plots_4326_Full.shp"
    #path_raster  ="/Volumes/My Passport/TempNaomi/Donnees/Drone/2018/Niakhar/2018_10_08/"
    #inRaster="orthoRGB_2018-10-08_georeferenced.tif"
    #annee='2018'
    inShp = "/Volumes/NAOMI/stage Israel /shapefiles/plotE4a.shp"
    path_raster  ="/Volumes/NAOMI/stage Israel /images drones/block E/E3 and E4/images_1712/"
    inRaster= "E3a_NDVI.tif"
    
    clip(inShp,path_raster,inRaster)