

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



#Tittar på deltagarnas åldersfördelning
tyskland_deltagare = df_anonym[df_anonym["NOC"] == "GER"]
sns.histplot(tyskland_deltagare["Age"], bins=20, kde=True)
plt.title("Åldersfördelning för tyska deltagare")
plt.xlabel("Ålder")
plt.ylabel("Antal deltagare")
plt.show()

#Filtrering av medaljer för lagsporter
tyskland_medaljer = df_anonym[df_anonym["NOC"] == "GER"]
tyskland_medaljer_per_lag = tyskland_medaljer.groupby(["Event", "Games"])["Medal"].nunique()
print(tyskland_medaljer_per_lag)

#Filtering av medaljer för lagsporter
tyskland_medaljer_per_lag_fotboll = tyskland_medaljer[tyskland_medaljer["Sport"] == "Hockey"].groupby(["Event", "Games"])["Medal"].nunique()
print(tyskland_medaljer_per_lag_fotboll)


# Välj ut 2-4 sporter
sporter = ["Athletics", "Cycling", "Tennis", "Shooting"]

# Filtrera data för Tyskland och Spanien
tyskland_data = df_anonym[df_anonym["NOC"] == "GER"]
spanien_data = df_anonym[df_anonym["NOC"] == "ESP"]

# Räkna medaljer för varje sport
tyskland_medaljer = tyskland_data[tyskland_data["Sport"].isin(sporter)].groupby("Sport")["Medal"].count()
spanien_medaljer = spanien_data[spanien_data["Sport"].isin(sporter)].groupby("Sport")["Medal"].count()

# Plotta medaljer med sns
sns.set()
plt.figure(figsize=(10,6))
sns.barplot(x="Sport", y="Medaljer", hue="Land", 
            data=pd.DataFrame({"Sport": tyskland_medaljer.index.tolist() 
                               + spanien_medaljer.index.tolist(),
                                "Medaljer": tyskland_medaljer.values.tolist() + spanien_medaljer.values.tolist(), 
                                "Land": ["Tyskland"] * len(tyskland_medaljer) + ["Spanien"] * len(spanien_medaljer)}))
plt.xlabel("Sport")
plt.ylabel("Medaljer")
plt.title("Medaljer i utvalda sporter")
plt.legend()
plt.show()

#Tittar på åldersfördelningen av deltagarna efter sport

# Välj ut 2-4 sporter
sporter = ["Athletics", "Cycling", "Tennis", "Shooting"]

# Filtrera data för Tyskland och Spanien
tyskland_data = df_anonym[df_anonym["NOC"] == "GER"]
spanien_data = df_anonym[df_anonym["NOC"] == "ESP"]

# Räkna antal deltagare per ålder och sport
tyskland_deltagare_per_ålder = tyskland_data[tyskland_data["Sport"].isin(sporter)].groupby(["Sport", "Age"])["ID"].count()
spanien_deltagare_per_ålder = spanien_data[spanien_data["Sport"].isin(sporter)].groupby(["Sport", "Age"])["ID"].count()

# Plotta ålder för Tyskland och Spanien
sns.set()
plt.figure(figsize=(10,6))
sns.lineplot(x="Age", y="Deltagare", hue="NOC", data=pd.DataFrame({"Age": tyskland_deltagare_per_ålder.index.get_level_values("Age").tolist() + spanien_deltagare_per_ålder.index.get_level_values("Age").tolist(), "Deltagare": tyskland_deltagare_per_ålder.values.tolist() + spanien_deltagare_per_ålder.values.tolist(), "NOC": ["Tyskland"] * len(tyskland_deltagare_per_ålder) + ["Spanien"] * len(spanien_deltagare_per_ålder)}))
plt.xlabel("Ålder")
plt.ylabel("Antal deltagare")
plt.title("Ålder för Tyskland och Spanien i valda sporter")
plt.legend()
plt.show()


