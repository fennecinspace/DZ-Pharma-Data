import re
import requests as rq
from bs4 import BeautifulSoup
from .common import Json


class LabInfoExtractor:
    site_url = "https://pharmnet-dz.com/"

    @classmethod
    def extract(cls, lab):
        res = rq.get(lab['link'])
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            
            data = soup.select('.col-lg-4.col-md-4.col-sm-4.col-xs-12')

            if len(data) > 2:
                img = data[0].select_one('img')
                if img:
                    lab['img'] = cls.site_url + img['src']

                content = data[1].text
                addr = content[content.find('Adresse')+8 :content.find('Tel')].strip('[ -\n]*')
                # tel = content[content.find('Tel')+4:content.find('Contact')].strip('[ -\n]*')
                web = content[content.find('Web')+4:].strip('[ -\n]*')

                tels = []
                for str_ in data[1].stripped_strings:
                    if any(char.isdigit() for char in str_.strip('[ -]')) and not any(char.isalpha() for char in str_.strip('[ -]')):
                        tels += [str_.strip('[ -]')]

                tels = ' - '.join(tels).replace('[ ]+', ' ')

                if addr != '':
                    lab['address'] = addr
                if tels != '':
                    lab['tel'] = tels
                if web != '':
                    lab['web'] = web
