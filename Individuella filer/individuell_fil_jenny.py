# En fil för att testa kod i innan det överförs till main filen för grupparbetet.
# Uppgift 1)

import pandas as pd
import hashlib as hl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df = pd.read_csv("Project_Olympic/athlete_events.csv")

# anonymisera kolumnerna med idrotternas namn
df_anonym = df.copy()
df_anonym["Name"] = df_anonym["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())

# print(f" Kolumner som anonymiseras: {df_anonym.columns}")

# sporter tyskland tagit flest medaljer i
tyskland_medaljer = df[(df["NOC"] == "GER") & (df["Medal"] != "NA")]

top_sporter = tyskland_medaljer["Sport"].value_counts().head(10)

print(top_sporter)

# Antalet medaljer tyskland tagit per OS
tyskland_medaljer_per_os = tyskland_medaljer.groupby(["Year"])["Medal"].count()
print(tyskland_medaljer_per_os)

# Historgram över Tysklands Åldrar i OS.
tyskland_age = tyskland_medaljer["Age"].hist(bins=120)
plt.title("Tysklands ålder i OS")
plt.xlabel("Ålder")
plt.ylabel("Antal")
plt.show()

# Uppgift 2)
