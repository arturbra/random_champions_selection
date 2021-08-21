import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import random


def get_champions(champions_url="https://app.mobalytics.gg/pt_br/lol/champions"):
    url = champions_url
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    selection = soup.find_all("div", {"class": "m-1lrsgsv"})
    selection = [str(a) for a in selection]
    all_champions = [re.search(">(.*?)<", champ).group(1) for champ in selection]
    all_champions = [c.lower().replace(" ", "") for c in all_champions]
    return all_champions


def filter_roles(champions, opgg_url = "https://br.op.gg/champion/statistics"):
    html_opgg = requests.get(opgg_url).content
    soup = BeautifulSoup(html_opgg, 'html.parser')
    selection = [a["href"] for a in soup.find_all("a", href=True)]
    champions_roles = {"top": [], "jungle": [], "mid": [], "adc": [], "support": []}
    for champ in champions:
        for role in champions_roles.keys():
            r = re.compile("/champion/" + champ + "/statistics/" + role)
            roles_list = list(filter(r.match, selection))
            if len(roles_list) != 0:
                champions_roles[role].append(champ)
    return champions_roles


def random_team(champion_roles):
    top = random.choice(champion_roles["top"])
    jungle = random.choice(champion_roles["jungle"])
    mid = random.choice(champion_roles["mid"])
    adc = random.choice(champion_roles["adc"])
    support = random.choice(champion_roles["support"])
    print("top: ", top, "\njungle:", jungle, "\nmid: ", mid, "\nadc: ", adc, "\nsupport: ", support)


if __name__ == "__main__":
    champions = get_champions()
    roles = filter_roles(champions)
    random_team(roles)
