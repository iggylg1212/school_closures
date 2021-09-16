# IMPORTS ######################################
import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn_pandas import DataFrameMapper
from itertools import product
import matplotlib.pyplot as plt
import random
import numpy
import subprocess
import numpy as np
import pickle
import csv
import sys
import os

# FILE PATHS ######################################
global LOCAL_PATH
LOCAL_PATH = os.path.expanduser("~") + "/Desktop/Schools/"

# IMPORT FUNCTIONS ################################
from Functions.cleaning_merging import cleaning_merging
from Functions.reg_sample import reg_sample
from Functions.regressions import regressions
from Functions.create_figures import create_figures
from Functions.df_mapper import df_mapper