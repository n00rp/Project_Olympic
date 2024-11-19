import dash
from dash import dcc
from dash import html
from dash import html
import dash_html_components as html
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import seaborn as sns
import hashlib as hl
import numpy as np


# Läs in data
file = pd.read_csv("Project_Olympic/athlete_events.csv")

# anonymisera kolumnerna med idrotternas namn
df = file.copy()
df["Name"] = df["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())

df_sporter = df[df["Sport"].isin(["Cross Country Skiing", "Football", "Sailing", "Handball"])]
df_sporter = df_sporter.dropna()
