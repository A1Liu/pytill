# -*- coding: utf-8 -*-

#%% Debugging

import pytest # Python testing framework

#%% Numbers

import numpy as np# Linear algebra library
import theano # Numerical computation, similar to numpy
import statsmodels.api # statistics
import scipy # Numerical routines
import sympy # symbolic computation
import functools # Function tools (built in module)

#%% Data

from sas7bdat import SAS7BDAT # import data from SAS files
import h5py # dada from HD5 files
import scipy.io # import MATLAB files scipy.io.readmat(<file_name>)
import json
import glob
import networkx as nx # Network storage and visualization
import nxviz as nxv # Networkx graph visualization library

import mr_clean as mrc # my package for checking out data before cleaning

#%% Visualization

import matplotlib.pyplot as plt # Plotting data
import seaborn as sns # Extension of pyplot for pandas df's
from bokeh.io import output_file, show # Interactive html of a graph
from bokeh.plotting import figure,ColumnDataSource # Interactive html of a graph
from bokeh.models import HoverTool,CategoricalColorMapper # Additional interactivity with model

# %% Importing

import importlib

#%% Web

import requests
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

#%% SQL

from sqlalchemy import create_engine
# Example: engine = create_engine('sqlite:///databaseName.sqlite')

#%% Randomness

from numpy.random import RandomState # a thread-safe object that has multiple randomness generation methods
import random.random # Thread-safe randomness, without statistics support
import secrets # Cryptographic randomness



#%% Machine Learning

import pandas as pd# Data analysis
import keras # Machine Learning
import sklearn # Machine learning: built on top of SciPy
import pybrain # Reinforcement learning, AI, neural networks

#%% NLP

import nltk # Natural language toolkit nltk.org
import re # Regular expresions
import ftfy # 'fixes text for you'