

df = pd.read_csv("../athlete_events.csv")


""" hashar namnen och droppar namn kolumnen """
hashes = df["Name"].apply(lambda client_num: hl.sha256(client_num.encode()).hexdigest())
df.insert(1, "SHA Hash Values", hashes)
drop = df.drop(columns= ["Name"])
df = drop

""" Tar alla unika sporter """
sports = df['Sport'].unique()

""" Tabell på antal medaljer per individ i tyskland """
ger_df = df[df["NOC"] == "GER"]
medal = ger_df["Medal"].isin(["Gold", "Silver", "Bronze"])
medals = ger_df[medal]
color1 = ["silver", "orange", "gold"]

"""" Björns filtrering av medaljer """
df_ger=df[df["NOC"]=="GER"]                                                 # Alla tyska deltagare
df_ger_medals=df_ger[df_ger["Medal"].isin(["Gold", "Silver", "Bronze"])]  

""" Tabell på medaljer som nation i Tyskland """
temp_df = ger_df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
ny_team_variabel = temp_df["Medal"].isin(["Gold", "Silver", "Bronze"])
ny_team_variabel = temp_df[ny_team_variabel]
test = ny_team_variabel.copy()


""" Tabell på medaljer """
test.loc[:, "Medaltot"] = 1
df_grouped = test.groupby(['Year', 'Medal']).sum().reset_index()
df_pivot = df_grouped.pivot(index='Year', columns='Medal', values='Medaltot')# Pivot = Year blir x-axeln och Medal blir kolumner med en valör i varje. Values(Medeltot) får summan av varje valör per år.
df_pivot_g = df_pivot["Gold"]
df_pivot_s = df_pivot["Silver"]
df_pivot_b = df_pivot["Bronze"]

""" Filtrering av medaljer inom skidor """
# Länder som tagit medalj i längdskidor
df_skidor=df[df["Sport"]=="Cross Country Skiing"]
df_skidor_medaljer=df_skidor[df_skidor["Medal"].isin(["Gold", "Silver", "Bronze"])]
df_skidor_medaljer["NOC"].value_counts()

fig3=px.bar(df_skidor_medaljer["NOC"].value_counts(), labels={"NOC": "Land", "value": "Antal medaljer"}, title=("Länder som tagit medalj i längdskidor"))
fig3.update_layout(showlegend=False)

# Definiera lista med vinter-OS
wo=["1924 Winter", "1928 Winter", "1932 Winter", "1936 Winter",
    "1948 Winter", "1952 Winter", "1956 Winter", "1960 Winter",
    "1964 Winter", "1968 Winter", "1972 Winter", "1976 Winter",
    "1980 Winter", "1984 Winter", "1988 Winter", "1992 Winter",
    "1994 Winter", "1998 Winter", "2002 Winter", "2006 Winter",
    "2010 Winter", "2014 Winter"]
