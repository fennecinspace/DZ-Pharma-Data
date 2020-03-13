import re
import string
import requests as rq
from bs4 import BeautifulSoup
from .common import Json


class MedsLinksExtractor:
    site_url = "https://pharmnet-dz.com/"
    letters = list(string.ascii_uppercase)

    @classmethod
    def extract_nb_pages(cls, letter):
        letter_link = "{}{}{}".format(cls.site_url, 'alphabet.aspx?char=', letter)
        
        res = rq.get(letter_link)
        
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "lxml")
            # getting number of pages
            return len(soup.select('a.btn.btn-xs.btn-warning')) + 1
        else:
            return 0


    @classmethod
    def extract_page_med_links(cls, letter, page):
        links = []
        letter_link = "{}{}{}".format(cls.site_url, 'alphabet.aspx?char=', letter)

        res = rq.get('{}&p={}'.format(letter_link, page))
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')

            med_items = soup.select('[scope="row"] > td:nth-of-type(1) > a:nth-of-type(1)')
            for med in med_items:
                links += ['{}{}'.format(cls.site_url, med['href'])]

        return links


    @classmethod
    def save(cls, links, save_path, letter = None):
        if letter:
            print('Letter {} | Saving      '.format(letter), end = "\r")
        else:
            print('Saving {}'.format(save_path))
        Json.save(save_path, links)

    @classmethod
    def extract(cls, save_path = None):
        links = {letter : [] for letter in cls.letters}
        
        for i, letter in enumerate(cls.letters):
            nb_pages = cls.extract_nb_pages(letter)
            
            for page in range(1, nb_pages + 1):
                print('Letter {} | Page [{:2}/{:2}]'.format(letter, page, nb_pages), end = "\r")
                links[letter] += cls.extract_page_med_links(letter, page)
                
            # save progress 
            if save_path:
                cls.save(links, save_path, letter)
                print('Letter {} | Done        '.format(letter))
        
        return links