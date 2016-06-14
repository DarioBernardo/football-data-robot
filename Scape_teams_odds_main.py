from web_scraper import scraper
from web_scraper import data_extractor
from web_scraper.malformed_page_exception import MalformedPageException
import logging

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

logging.info("Scraping odds for each team.")
teams_odds_tree = scraper.scrap_teams_odds()
data_extractor.extract_teams_odds(teams_odds_tree)

print("Execution terminated.")
