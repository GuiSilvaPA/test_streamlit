import streamlit as st
import pandas    as pd
from io import BytesIO
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib
import numpy as np
from fpdf import FPDF
import base64
import tempfile

import sys
sys.path.append('C:/Users/Scarlet/Desktop/FEV/Code/')
# sys.path.append('C:/Users/Scarlet/Desktop/FEV/Review/')

from ProcessCurrentAngleSweep import *
from Variables import *
from APTIV import *