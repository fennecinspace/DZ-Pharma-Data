import requests as req
from bs4 import BeautifulSoup
import os, json, re

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MEDS_FILE = os.path.join(BASE_DIR, 'data', 'meds.json')
LABS_FILE = os.path.join(BASE_DIR, 'data', 'labs.json')
SITE_URL = "https://pharmnet-dz.com/"

new_labs_file = False
if new_labs_file:
    print('Creating Labs File')
    with open(MEDS_FILE, 'r') as f:
        meds_data = json.loads(f.read())

    labs = []
    for char, meds in meds_data.items():
        for med in meds:
            if 'lab' in med:
                labs += [med['lab']]

    labs = [ dict(tpl) for tpl in set( tuple(item.items()) for item in labs )]

    with open(LABS_FILE, 'w') as f:
        f.write(json.dumps(labs))

    print()
    
with open(LABS_FILE, 'r') as f:
    labs = json.loads(f.read())

for i in range(len(labs)):
    print('\r LAB [{:4}/{:4}]'.format(i+1, len(labs)), end = '')
    if all(e not in labs[i] for e in ['img', 'address']):
        page = req.get(labs[i]['link'])
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'lxml')
            data = soup.select('.col-lg-4.col-md-4.col-sm-4.col-xs-12')
            if len(data) > 2:
                img = data[0].select_one('img')
                if img:
                    labs[i]['img'] = SITE_URL + img['src']

                content = data[1].text
                addr = content[content.find('Adresse')+8 :content.find('Tel')].strip('[ -\n]*')
                # tel = content[content.find('Tel')+4:content.find('Contact')].strip('[ -\n]*')
                web = content[content.find('Web')+4:].strip('[ -\n]*')

                tels = [
                    str_.strip('[ -]') for str_ in data[1].stripped_strings 
                    if any(char.isdigit() for char in str_.strip('[ -]')) 
                    and not any(char.isalpha() for char in str_.strip('[ -]')) 
                ]

                tels = ' - '.join(tels).replace('[ ]+', ' ')

                if addr != '':
                    labs[i]['address'] = addr
                if tels != '':
                    labs[i]['tel'] = tels
                if web != '':
                    labs[i]['web'] = web

            with open(LABS_FILE, 'w') as f:
                f.write(json.dumps(labs))

print()