import re
import requests as rq
from bs4 import BeautifulSoup
from .common import Json


class MedInfoExtractor:
    site_url = "https://pharmnet-dz.com/"

    @classmethod
    def extract_img(cls, soup, med):
        tmp = soup.find(attrs={'style' : 'max-width:200px; max-height:200px; display:block; margin:0 auto; margin-bottom:20px;'})            
        if tmp:
            med['img'] = cls.site_url + tmp['src']


    @classmethod
    def extract_notice(cls, soup, med):
        tmp = soup.find(attrs={'href' : re.compile("notice*")})
        if tmp:
            med['notice'] = cls.site_url + tmp['href']


    @classmethod
    def scrap_left_section(cls, soup, med): 
        section = soup.find('div', class_ ='col-lg-7 col-md-7 col-sm-8 col-xs-12')
        tmp = section.find_all('a')
        if len(tmp) > 0:
            med['lab'] = {
                'name': tmp[0].text.strip(),
                'link': cls.site_url + tmp[0]['href'],
            }
        if len(tmp) > 1:
            med['class'] = {'pharmacological': tmp[1].text.strip()}
        if len(tmp) > 2:
            med['class']['therapeutic'] = tmp[2].text.strip()
        if len(tmp) > 3:
            med['generic'] = tmp[3].text.strip()


    @classmethod
    def scrap_right_section(cls, soup, med): 
        section = soup.find('div', class_ ='col-lg-5 col-md-5 col-sm-4 col-xs-12')
        all_lines = str(section).splitlines()
        for line in all_lines:
            if 'Commercialisation' in line:
                if 'darkgreen' in line:
                    med['commercialisation'] = True
                elif 'darkred' in line:
                    med['commercialisation'] = False
                else:
                    med['commercialisation'] = None
            if 'Remboursable' in line:
                if 'darkgreen' in line:
                    med['refundable'] = True
                elif 'darkred' in line:
                    med['refundable'] = False
                else:
                    med['refundable'] = None

    
    @classmethod
    def scrap_commun_lines(cls, soup, med):
        r_section = soup.find('div', class_ ='col-lg-5 col-md-5 col-sm-4 col-xs-12')
        l_section = soup.find('div', class_ ='col-lg-7 col-md-7 col-sm-8 col-xs-12')
        all_lines = r_section.text.splitlines() + l_section.text.splitlines()
        all_lines = [line.strip() for line in all_lines if line.strip() != '']

        for line in all_lines:
            if 'Liste' in line:
                med['list'] = line[line.find(':') + 1:].strip()
            
            if 'Pays' in line:
                med['country'] = line[line.find(':') + 1:].strip()
                
            if 'Tarif' in line:
                trif_tmp = line[line.find(':') + 1:].strip()
                if trif_tmp.lower() in ['0 da', "-- da", "n/a", 'da']:
                    med['reference_rate'] = None
                else:
                    med['reference_rate'] = trif_tmp

            if 'PPA' in line and line[line.find(':') + 1:].strip().lower() not in ['da', '']:
                ppa_tmp = line[line.find(':') + 1:].strip()
                if ppa_tmp.lower() in ['0 da', "-- da", "n/a", 'da']:
                    med['ppa'] = None
                else:
                    med['ppa'] = ppa_tmp
                
            if 'Enregistrement' in line:
                med['registration'] = line[line.find(':') + 1:].strip()
            
            if 'Commercial' in line:
                med['commercial_name'] = line[line.find(':') + 1:].strip()

            if 'Code' in line:
                med['dci'] = line[line.find(':') + 1:].strip()

            if 'Forme' in line:
                med['form'] = line[line.find(':') + 1:].strip().strip('.')

            if 'Dosage' in line:
                med['dosage'] = line[line.find(':') + 1:].strip()

            if 'Conditionnement' in line:
                med['conditioning'] = line[line.find(':') + 1:].strip()


    @classmethod
    def scrap_med_page(cls, link):
        res = rq.get(link)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "lxml")

            ## name
            tmp = soup.find(attrs={'style' : 'text-shadow: 3px 3px rgb(216, 228, 237); padding-left: 10px; padding-right: 10px; margin-top:0px;'})
            if tmp:

                med = {'name': tmp.text.strip(), 'link': link}

                cls.extract_img(soup,med)
                cls.extract_notice(soup, med)
                cls.scrap_left_section(soup, med)
                cls.scrap_right_section(soup, med)
                cls.scrap_commun_lines(soup, med)
                
                return med