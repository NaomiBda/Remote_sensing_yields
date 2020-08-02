#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 12:22:03 2020

@author: naomiberda
"""


import pandas as pd
import csv
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
import reglin as rgl
from sklearn.linear_model import LinearRegression


cv=KFold(5)
cross_val_score(LinearRegression() ,X,y,cv=cv)
                  
