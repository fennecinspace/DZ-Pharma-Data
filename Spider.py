import os
import string
import re
import json
import requests as rq
from bs4 import BeautifulSoup

SITE_URL = "https://pharmnet-dz.com/"
LETTERS = list(string.ascii_uppercase)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MED_LINKS_DB = os.path.join(BASE_DIR, 'data', 'links.json')
MED_INFOS_DB = os.path.join(BASE_DIR, 'data', 'meds.json')


class Json:
    @classmethod
    def save(cls, file_path, data):
        try:
            with open(file_path, 'w') as f:
                f.write(json.dumps(data))
                return True
        except Exception as e:
            print("Could not save to JSON file !")


    @classmethod
    def read(cls, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.loads(f.read())
        except Exception as e:
            print("Could not read from JSON file !")
            return {}



class MedsLinksExtractor:
    def __init__(self, save_path = MED_LINKS_DB, letters = LETTERS):
        self.links = { letter : [] for letter in letters }
        self.save_path = save_path
        self.letters = letters


    def extract_nb_pages(self, letter):
        letter_link = "{}{}{}".format(SITE_URL, 'alphabet.aspx?char=', letter)
            
        res = rq.get(letter_link)
        soup = BeautifulSoup(res.content, "lxml")
        
        # getting number of pages
        return len(soup.select('a.btn.btn-xs.btn-warning')) + 1


    def extract_page_med_links(self, letter, page):
        letter_link = "{}{}{}".format(SITE_URL, 'alphabet.aspx?char=', letter)

        res = rq.get('{}&p={}'.format(letter_link, page))
        soup = BeautifulSoup(res.content, 'lxml')

        med_items = soup.select('[scope="row"] > td:nth-of-type(1) > a:nth-of-type(1)')
        for med in med_items:
            self.links[letter] += ['{}{}'.format(SITE_URL, med['href'])]


    def save(self, letter):
        print('Letter {} | Saving      '.format(letter), end = "\r")
        Json.save(self.save_path, self.links)


    def extract(self):
        for i, letter in enumerate(self.letters):
            nb_pages = self.extract_nb_pages(letter)
            
            for page in range(1, nb_pages + 1):
                print('Letter {} | Page [{:2}/{:2}]'.format(letter, page, nb_pages), end = "\r")
                self.extract_page_med_links(letter, page)
                
            # save progress 
            self.save(letter)
            print('Letter {} | Done        '.format(letter))




if __name__ == "__main__":
    # Extracting Links of all Med Pages
    links_extractor = MedsLinksExtractor()
    links_extractor.extract()