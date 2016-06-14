import requests
from lxml import html

def scrap_by_game_name(game_name):
    link = 'http://www.oddschecker.com/football/euro-2016/{}/winner'.format(game_name)
    page = requests.get(link)
    tree = html.fromstring(page.content)
    return tree


def scrap_teams_odds():
    link = 'http://www.oddschecker.com/football/euro-2016/winner'
    page = requests.get(link)
    tree = html.fromstring(page.content)
    return tree



