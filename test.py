# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 13:06:34 2016

@author: 64510
"""

import mysql.connector
import pandas as pd
import numpy as np
from numpy import random
from pandas import Series
from pandas import DataFrame

values = []
for x in range(0,5):
    for y in range(0,5):
        values.append((x,y))
random.shuffle(values)
