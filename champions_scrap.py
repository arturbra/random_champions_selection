import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import random

url_champions = "https://lol.fandom.com/wiki/Portal:Champions/List"
html_champions = requests.get(url_champions).content
df_list = pd.read_html(html_champions)
df = df_list[-1]
champions = df["Champion"]
champions = [champ.lower().replace(" ", "") for champ in champions]

url_opgg = "https://br.op.gg/champion/statistics"
html_opgg = requests.get(url_opgg).content
soup = BeautifulSoup(html_opgg, 'html.parser')
soup_txt = str(soup)
string = "/champion/" + champions[0] + "/statistics"
string in soup_txt

champions_roles = {"top": [], "jungle": [], "mid": [], "adc": [], "support": []}
selection = [a["href"] for a in soup.find_all("a", href=True)]
for champ in champions:
    for role in champions_roles.keys():
        r = re.compile("/champion/" + champ + "/statistics/" + role)
        roles_list = list(filter(r.match, selection))
        if len(roles_list) != 0:
            champions_roles[role].append(champ)


def random_team(champion_roles):
    top = random.choice(champion_roles["top"])
    jungle = random.choice(champion_roles["jungle"])
    mid = random.choice(champion_roles["mid"])
    adc = random.choice(champion_roles["adc"])
    support = random.choice(champion_roles["support"])
    print("top: ", top, "\njungle:", jungle, "\nmid: ", mid, "\nadc: ", adc, "\nsupport: ", support)
