# En fil för att testa kod i innan det överförs till main filen för grupparbetet.

import pandas as pd
import hashlib as hl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df = pd.read_csv("Project_Olympic/athlete_events.csv")

# anonymisera kolumnerna med idrotternas namn
df_anonym = df.copy()
df_anonym["Name"] = df_anonym["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())

print(f" Kolumner som anonymiseras: {df_anonym.columns}")

# sporter tyskland tagit flest medaljer i
