# En fil för att testa kod i innan det överförs till main filen för grupparbetet.
# Uppgift 1)

import pandas as pd
import hashlib as hl
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Project_Olympic/athlete_events.csv")

# anonymisera kolumnerna med idrotternas namn
df_anonym = df.copy()
df_anonym["Name"] = df_anonym["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())

# print(f" Kolumner som anonymiseras: {df_anonym.columns}")

# sporter tyskland tagit flest medaljer i
tyskland_medaljer = df_anonym[(df_anonym["NOC"] == "GER") & (df["Medal"] != "NA")]

top_sporter = tyskland_medaljer["Sport"].value_counts().head(10)

print(f"Sporter tyskland tagit flest medaljer: {top_sporter}")

# Antalet medaljer tyskland tagit per OS
tyskland_medaljer_per_os = tyskland_medaljer.groupby(["Year"])["Medal"].count()
print(f"Antalet medaljer tyskland tagit per OS: {tyskland_medaljer_per_os}")

# Historgram över Tysklands Åldrar i OS.
tyskland_age = tyskland_medaljer["Age"].hist(bins=140)
plt.title("Tysklands ålder i OS")
plt.xlabel("Ålder")
plt.ylabel("Antal")
plt.show()

# Uppgift 2)  Välj 2-4 sporter och skapa lämpliga grafer/diagram för att visualisera exempelvis:
#  medaljfördelning mellan länder i sporterna

df_sporter = df_anonym[df_anonym["Sport"].isin(["Ice Hockey", "Football", "Sailing", "Handball"])]

# Filtrera data för att endast inkludera Tyskland, Sverige, Norge och Danmark.
df_sporter_de_se = df_sporter[df_sporter["NOC"].isin(["GER", "SWE", "NOR", "DEN"])]

# Plottar resultat för att visualisera medaljfördelningen mellan länder i dessa sporter:
sns.set_theme(style="darkgrid")
sns.lineplot(x="Sport", y="Medal", hue="NOC", data=df_sporter_de_se, palette="pastel")

plt.show()

df_grouped = df_anonym.groupby(["Year", "NOC"])["Medal"].count().reset_index()

# Gruppera data efter år och räkna antalet medaljer
df_tyskland = df_grouped[df_grouped["NOC"] == "GER"]

# Plottar resultat för att visualisera medaljfördelningen mellan åren:
plt.figure(figsize=(12, 14))
sns.set_theme(style="darkgrid")
sns.barplot(x="Year", y="Medal", data=df_tyskland, palette="pastel")

plt.title("Antal medaljer för Tyskland i OS")
plt.xlabel("År")
plt.ylabel("Antal medaljer")

plt.tight_layout()
plt.show()

print(f"Antal medaljer som tyskland tagit under åren i OS: {df_tyskland}")

#  åldersfördelning i sporterna
df_sporter = df_anonym[df_anonym["Sport"].isin(["Ice Hockey", "Football", "Sailing", "Handball"])]
sns.set_theme(style="darkgrid")
sns.histplot(x="Age", hue="Sport", data=df_sporter, bins=20, kde=True)

plt.title("Åldersfördelning i sporterna i OS")
plt.xlabel("Ålder")
plt.ylabel("Antal deltagare")
plt.show()

# Räknar antalet män och kvinnor över tid i OS.
df_os_kon = df_sporter.groupby(["Year", "Season", "Sex"])["Name"].count().reset_index()
df_os_kon = df_os_kon.rename(columns={"Name": "Antal"})

# print(df_os_kon)

sommar_os = df_os_kon[df_os_kon["Season"] == "Summer"]
plt.figure(figsize=(12, 14), dpi=100)
plt.subplot(3, 2, 1)
sns.lineplot(x="Year", y="Antal", hue="Sex", data=sommar_os, palette=["red", "blue"])
plt.title("Könsfördelningen i sommar OS över tid")
plt.xlabel("År")
plt.ylabel("Antal deltagare")

vinter_os = df_os_kon[df_os_kon["Season"] == "Winter"]
plt.subplot(3, 2, 2)
sns.lineplot(x="Year", y="Antal", hue="Sex", data=vinter_os, palette=["blue", "red"])
plt.title("Könsfördelningen i vinter OS över tid")
plt.xlabel("År")
plt.ylabel("Antal deltagare")

plt.tight_layout()
plt.show()


print(f"Sommar OS: {sommar_os}")
print(f"Vinter OS: {vinter_os}")


