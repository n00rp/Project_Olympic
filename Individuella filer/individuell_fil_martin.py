

# En fil för att testa kod i innan det överförs till main filen för grupparbetet.

import pandas as pd
import hashlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Läs in data från filen
df = pd.read_csv("Project_Olympic/athlete_events.csv")

#Anonymisera kolumnen med idrottarnas namn
df_anonym = df.copy()
df_anonym["Name"] = df_anonym["Name"].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())


print(df_anonym.columns)

#Tittar på Tysklands bästa idrotter
medaljer_per_land_tyskland = df_anonym[df_anonym["NOC"] == "GER"].groupby("Sport")["Medal"].value_counts().sort_values(ascending=False)
print(medaljer_per_land_tyskland.head(5))
#Tittar på hur många medaljer Tyskland fick i olika OS
medaljer_per_os_tyskland = df_anonym[df_anonym["NOC"] == "GER"].groupby("Games")["Medal"].count()
print(medaljer_per_os_tyskland)




tyskland_deltagare = df_anonym[df_anonym["NOC"] == "GER"]
sns.histplot(tyskland_deltagare["Age"], bins=20, kde=True)
plt.title("Åldersfördelning för tyska deltagare")
plt.xlabel("Ålder")
plt.ylabel("Antal deltagare")
plt.show()




