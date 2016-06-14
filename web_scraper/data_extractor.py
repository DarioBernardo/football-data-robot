import numpy as np
import pandas as pd
import os.path
from datetime import datetime
import logging

from web_scraper.malformed_page_exception import MalformedPageException


def extract_datapoint_for_winning_market(tree):
    event_name_xpath = '//div[@id="oddsTableContainer"]/table/@data-sname'

    odds_providers_xpath = '//div[@id="oddsTableContainer"]/table/thead/tr[@class="eventTableHeader"]/td/@data-bk'

    odds_fraction_xpath = '//div[@id="oddsTableContainer"]/table/tbody/tr/td/@data-o'
    odds_number_xpath = '//div[@id="oddsTableContainer"]/table/tbody/tr/td/@data-odig'
    bet_name_xpath = '//div[@id="oddsTableContainer"]/table/tbody/tr/td[@class="sel nm"]/span/@data-name'

    event_names_list = tree.xpath(event_name_xpath)

    if len(event_names_list) != 1:
        raise MalformedPageException("The event is not available anymore!")

    event_name = event_names_list[0]
    odds_providers = tree.xpath(odds_providers_xpath)

    odds_fraction = tree.xpath(odds_fraction_xpath)
    odds_number = tree.xpath(odds_number_xpath)
    bet_name = tree.xpath(bet_name_xpath)

    if len(odds_providers) == 0:
        raise MalformedPageException("The event is not available anymore!")

    reshaped_odds_fraction = np.reshape(odds_fraction, (3, len(odds_providers)))
    reshaped_odds_number = np.reshape(odds_number, (3, len(odds_providers)))


    # print(event_name)
    # print(odds_providers)
    # print(reshaped_odds_number)
    # print(bet_name)

    for counter, betting_odds in enumerate(reshaped_odds_number):
        filename = "data/{}_odds_{}.csv".format(event_name.replace(" ", "_"), bet_name[counter])
        file_exists = os.path.isfile(filename)

        if file_exists:
            # print("exists!")
            new_csv_row = "{},{}\n".format(datetime.now().replace(second=0, microsecond=0), ",".join(betting_odds))
            fd = open(filename, 'a')
            fd.write(new_csv_row)
            fd.close()
        else:
            df = pd.DataFrame(data=[betting_odds], columns=odds_providers, index=[datetime.now().replace(second=0, microsecond=0)])
            df.to_csv(filename, sep=',', encoding='utf-8')


def extract_teams_odds(tree):
    odds_providers_xpath = '//div[@id="oddsTableContainer"]/table/thead/tr[@class="eventTableHeader"]/td/@data-bk'
    odds_number_xpath = '//div[@id="oddsTableContainer"]/table/tbody/tr/td/@data-odig'
    odds_teams_xpath = '//div[@id="oddsTableContainer"]/table/tbody/tr/td/a/@data-name'

    odds_providers = tree.xpath(odds_providers_xpath)
    odds_number = tree.xpath(odds_number_xpath)
    team_names = tree.xpath(odds_teams_xpath)

    if len(odds_providers) == 0 or len(odds_number) == 0 or len(team_names) == 0:
        raise MalformedPageException("The event is not available anymore!")

    reshaped_odds_number = np.reshape(odds_number, (len(team_names), len(odds_providers)))


    if(reshaped_odds_number.shape[0] != len(team_names) or reshaped_odds_number.shape[1] != len(odds_providers)):
        raise MalformedPageException("The number of rows and columns do not match! table shape <{}>, "
                                     "odds providers: {} and teams: {}".format(
            reshaped_odds_number.shape,
            team_names,
            odds_providers
        ))

    # print(odds_providers)
    # print(team_names)
    # print(reshaped_odds_number)

    for counter, betting_odds in enumerate(reshaped_odds_number):
        team = team_names[counter]

        logging.info("Storing odds for team {}".format(team))

        filename = "data/{}_odds.csv".format(team.replace(" ", "_"))
        file_exists = os.path.isfile(filename)

        if file_exists:
            # print("exists!")
            new_csv_row = "{},{}\n".format(datetime.now().replace(second=0, microsecond=0), ",".join(betting_odds))
            fd = open(filename, 'a')
            fd.write(new_csv_row)
            fd.close()
        else:
            df = pd.DataFrame(data=[betting_odds], columns=odds_providers,
                              index=[datetime.now().replace(second=0, microsecond=0)])
            df.to_csv(filename, sep=',', encoding='utf-8')

