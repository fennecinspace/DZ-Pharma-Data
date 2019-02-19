import requests as req
from bs4 import BeautifulSoup
import os, json, re

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LINKS_FILE = os.path.join(BASE_DIR, 'links.json')
MEDS_FILE = os.path.join(BASE_DIR, 'meds.json')
SITE_URL = "https://pharmnet-dz.com/"

medications = []

with open(LINKS_FILE, 'r') as f:
    meds_links = json.loads(f.read())

for char, char_links in meds_links.items():
    for i, med_url in enumerate(char_links):
        print('\rLetter {} | Medications [{:4}/{:4}]'.format(char, i+1, len(char_links)), end = '')
        try:
            page_to_bs4 = req.get(med_url)
            if page_to_bs4.status_code == 200:
                med_page = BeautifulSoup( page_to_bs4.content, "lxml")
                left_info = med_page.find('div', class_ ='col-lg-7 col-md-7 col-sm-8 col-xs-12')
                right_info = med_page.find('div', class_ ='col-lg-5 col-md-5 col-sm-4 col-xs-12')

                ## getting headline name
                tmp = med_page.find(attrs={'style' : 'text-shadow: 3px 3px rgb(216, 228, 237); padding-left: 10px; padding-right: 10px; margin-top:0px;'})

                if tmp:
                    elem = {'nom': tmp.text, 'link': med_url}

                    ## getting Image
                    tmp = med_page.find(attrs={'style' : 'max-width:200px; max-height:200px; display:block; margin:0 auto; margin-bottom:20px;'})
                    if tmp:
                        elem['Img'] = SITE_URL + tmp['src']

                    ## getting headline name
                    tmp = med_page.find(attrs={'href' : re.compile("notice*")})
                    if tmp:
                        elem['Notice'] = SITE_URL + tmp['href']

                    ## getting  Main Data
                    tmp = left_info.find_all('a')
                    if len(tmp) > 0:
                        elem['Laboratoire'] = tmp[0].text

                    if len(tmp) > 1:
                        elem['C.Pharmacologique'] = tmp[1].text

                    if len(tmp) > 2:
                        elem['C.Therapeutique'] = tmp[2].text
                        
                    if len(tmp) > 3:
                        elem['Info'] = tmp[3].text

                    ## getting all page additional data
                    all_lines = right_info.text.splitlines() + left_info.text.splitlines()
                    all_lines = [line.strip() for line in all_lines if line.strip() != '']

                    to_find = ['Liste', 'Pays', 'Tarif de reference', 'PPA', 'Num Enregistrement', 'Nom Commercial', 'Code DCI', 'Forme', 'Dosage', 'Conditionnement']   
                    elem.update(dict([(elem, None) for elem in to_find]))              

                    for line in all_lines:
                        if 'Liste' in line:
                            elem['Liste'] = line[line.find(':') + 1:].strip()
                        
                        if 'Pays' in line:
                            elem['Pays'] = line[line.find(':') + 1:].strip()
                            
                        if 'Tarif' in line and line[line.find(':') + 1:].strip().lower() not in ['da', '']:
                            elem['Tarif de reference'] = line[line.find(':') + 1:].strip()

                        if 'PPA' in line and line[line.find(':') + 1:].strip().lower() not in ['da', '']:
                            elem['PPA'] = line[line.find(':') + 1:].strip()
                            
                        if 'Enregistrement' in line:
                            elem['Num Enregistrement'] = line[line.find(':') + 1:].strip()
                        
                        if 'Commercial' in line:
                            elem['Nom Commercial'] = line[line.find(':') + 1:].strip()

                        if 'Code' in line:
                            elem['Code DCI'] = line[line.find(':') + 1:].strip()

                        if 'Forme' in line:
                            elem['Forme'] = line[line.find(':') + 1:].strip().strip('.')

                        if 'Dosage' in line:
                            elem['Dosage'] = line[line.find(':') + 1:].strip()

                        if 'Conditionnement' in line:
                            elem['Conditionnement'] = line[line.find(':') + 1:].strip()

                    html_lines = str(right_info).splitlines()
                    for line in html_lines:
                        if 'Commercialisation' in line:
                            if 'darkgreen' in line:
                                elem['Commercialisation'] = True
                            elif 'darkred' in line:
                                elem['Commercialisation'] = False
                            else:
                                elem['Commercialisation'] = None
                        if 'Remboursable' in line:
                            if 'darkgreen' in line:
                                elem['Remboursable'] = True
                            elif 'darkred' in line:
                                elem['Remboursable'] = False
                            else:
                                elem['Remboursable'] = None
                    
                    medications += [elem]
        except Exception as e:
            print('\n{}:'.format(med_url), e)

    try:
        print(' --> [ Saving ] ', end = "")
        with open(MEDS_FILE, 'w') as f:
            f.write(json.dumps(medications))
        print('\b'*16 + ' --> [  Done  ] ')
    except:
        print(' --> [ Could not save ] ')