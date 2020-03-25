#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 09:24:17 2020

@author: naomiberda
"""

import geopandas 
import rasterio
from rasterio.mask import mask
import json

def clip (inShp, inRaster):
    
    df = geopandas.read_file(inShp)
    with rasterio.open(inRaster) as ds:
        profile = ds.profile
        for index, row in df.iterrows():
            coords = [json.loads(df.to_json())['features'][index]['geometry']]
            masked, out_transform = mask(dataset=ds, shapes=coords, crop=True)
            profile.update(transform=out_transform,height=masked.shape[1],width=masked.shape[2])
            #id_placette=row.ID_Placett.replace('/','_')
            outName = inRaster.replace('.tif',f'_{row.IDPlacette}.tif')
            with rasterio.open(outName,'w',**profile) as outds :
                for i in range (ds.count):
                    outds.write(masked[i,:,:],i+1)
                    
if __name__=='__main__' :
    inShp = "/Volumes/My Passport/TempNaomi/Donnees/Shapefiles/2019/Subplots.shp"
    inRaster="/Volumes/My Passport/TempNaomi/Donnees/Drone/2019/Niakhar/19-10-17/2019_10_17.tif"
    clip(inShp,inRaster)