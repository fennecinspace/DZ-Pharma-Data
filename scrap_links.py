import requests as req
from bs4 import BeautifulSoup
import os, json

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LINKS_FILE = os.path.join(BASE_DIR, 'data', 'links.json')

SITE_URL  = "https://pharmnet-dz.com/"
chars = [ chr(i) for i in range(65,91) ]
links = ["{}{}{}".format(SITE_URL, 'alphabet.aspx?char=', char) for char in chars]

medications_links = {}

for c, link in enumerate(links):
    meds_lst = req.get(link)
    if meds_lst.status_code == 200:
        soup = BeautifulSoup(meds_lst.content, "lxml")

        # getting number of pages
        nb_pages = len(soup.select('a.btn.btn-xs.btn-warning')) + 1

        # going through page by page
        for i in range(1, nb_pages + 1):
            print('Letter {} | Page [{:2}/{:2}]'.format(chars[c], i, nb_pages), end = "\r")
            meds_lst_page = req.get('{}&p={}'.format(link, i))
            if meds_lst_page.status_code == 200:
                meds_list_soup = BeautifulSoup(meds_lst_page.content, 'lxml')
                meds_in_page = meds_list_soup.select('[scope="row"] > td:nth-of-type(1) > a:nth-of-type(1)')
                for med in meds_in_page:
                    if chars[c] in medications_links:
                        medications_links[chars[c]] += [{'link':'{}{}'.format(SITE_URL, med['href'])}]
                    else:
                        medications_links[chars[c]] = [{'link':'{}{}'.format(SITE_URL, med['href'])}]
    
    print('Letter {} | Saving      '.format(chars[c]), end = "\r")
    with open(LINKS_FILE, 'w') as f:
        f.write(json.dumps(medications_links))
    print('Letter {} | Done        '.format(chars[c]))