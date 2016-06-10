from web_scraper import scraper
from web_scraper import data_extractor
from web_scraper.malformed_page_exception import MalformedPageException
import logging
import time

LOG_FILENAME = "log.txt"

logging.basicConfig(filename=LOG_FILENAME, format='%(levelname)s: %(asctime)s  -  %(message)s', datefmt='%m-%d %H:%M',
                    level=logging.ERROR)

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

while (True):
    games_list = "games_to_follow.txt"
    with open(games_list) as f:
        for line in f.readlines():
            game_name = line.strip('\n')
            msg = "Collecting data for game:  <{}>".format(game_name)
            logging.info(msg)
            print(msg)

            # page_tree = scraper.scrap_by_game_name("albania-v-switzerland")
            page_tree = scraper.scrap_by_game_name(game_name)

            try:
                data_extractor.extract_datapoint_for_winning_market(page_tree)
            except MalformedPageException as e:
                logging.error("The event {} was not found".format(game_name))

    print("Now sleeping")
    time.sleep(540)  # Pause current thread for 9 minutes
