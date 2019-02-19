import requests as req
from bs4 import BeautifulSoup
import os, json, re

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MEDS_FILE = os.path.join(BASE_DIR, 'meds.json')
SITE_URL = "https://pharmnet-dz.com/"

with open(MEDS_FILE, 'r') as f:
    medications = json.loads(f.read())

for char, char_links in medications.items():
    for i, med in enumerate(char_links):
        print('\rLetter {} | Medications [{:4}/{:4}]'.format(char, i+1, len(char_links)), end = '')
        if 'Nom' in med:
            continue
        try:
            page_to_bs4 = req.get(med['link'])
            if page_to_bs4.status_code == 200:
                med_page = BeautifulSoup( page_to_bs4.content, "lxml")
                left_info = med_page.find('div', class_ ='col-lg-7 col-md-7 col-sm-8 col-xs-12')
                right_info = med_page.find('div', class_ ='col-lg-5 col-md-5 col-sm-4 col-xs-12')

                ## getting headline name
                tmp = med_page.find(attrs={'style' : 'text-shadow: 3px 3px rgb(216, 228, 237); padding-left: 10px; padding-right: 10px; margin-top:0px;'})

                if tmp:
                    med = {'Nom': tmp.text, 'link': med['link']}

                    ## getting Image
                    tmp = med_page.find(attrs={'style' : 'max-width:200px; max-height:200px; display:block; margin:0 auto; margin-bottom:20px;'})
                    if tmp:
                        med['Img'] = SITE_URL + tmp['src']

                    ## getting headline name
                    tmp = med_page.find(attrs={'href' : re.compile("notice*")})
                    if tmp:
                        med['Notice'] = SITE_URL + tmp['href']

                    ## getting  Main Data
                    tmp = left_info.find_all('a')
                    if len(tmp) > 0:
                        med['Laboratoire'] = tmp[0].text

                    if len(tmp) > 1:
                        med['C.Pharmacologique'] = tmp[1].text

                    if len(tmp) > 2:
                        med['C.Therapeutique'] = tmp[2].text
                        
                    if len(tmp) > 3:
                        med['Info'] = tmp[3].text

                    ## getting all page additional data
                    all_lines = right_info.text.splitlines() + left_info.text.splitlines()
                    all_lines = [line.strip() for line in all_lines if line.strip() != '']

                    to_find = ['Liste', 'Pays', 'Tarif de reference', 'PPA', 'Num Enregistrement', 'Nom Commercial', 'Code DCI', 'Forme', 'Dosage', 'Conditionnement']   
                    med.update(dict([(med, None) for med in to_find]))              

                    for line in all_lines:
                        if 'Liste' in line:
                            med['Liste'] = line[line.find(':') + 1:].strip()
                        
                        if 'Pays' in line:
                            med['Pays'] = line[line.find(':') + 1:].strip()
                            
                        if 'Tarif' in line and line[line.find(':') + 1:].strip().lower() not in ['da', '']:
                            med['Tarif de reference'] = line[line.find(':') + 1:].strip()

                        if 'PPA' in line and line[line.find(':') + 1:].strip().lower() not in ['da', '']:
                            med['PPA'] = line[line.find(':') + 1:].strip()
                            
                        if 'Enregistrement' in line:
                            med['Num Enregistrement'] = line[line.find(':') + 1:].strip()
                        
                        if 'Commercial' in line:
                            med['Nom Commercial'] = line[line.find(':') + 1:].strip()

                        if 'Code' in line:
                            med['Code DCI'] = line[line.find(':') + 1:].strip()

                        if 'Forme' in line:
                            med['Forme'] = line[line.find(':') + 1:].strip().strip('.')

                        if 'Dosage' in line:
                            med['Dosage'] = line[line.find(':') + 1:].strip()

                        if 'Conditionnement' in line:
                            med['Conditionnement'] = line[line.find(':') + 1:].strip()

                    html_lines = str(right_info).splitlines()
                    for line in html_lines:
                        if 'Commercialisation' in line:
                            if 'darkgreen' in line:
                                med['Commercialisation'] = True
                            elif 'darkred' in line:
                                med['Commercialisation'] = False
                            else:
                                med['Commercialisation'] = None
                        if 'Remboursable' in line:
                            if 'darkgreen' in line:
                                med['Remboursable'] = True
                            elif 'darkred' in line:
                                med['Remboursable'] = False
                            else:
                                med['Remboursable'] = None
                    
                    medications[char][i] = med
                    with open(MEDS_FILE, 'w') as f:
                        f.write(json.dumps(medications))

        except Exception as e:
            print('\n{}:'.format(med['link']), e)
    print()
    # try:
    #     print(' --> [ Saving ] ', end = "")
        
    # except:
    #     print(' --> [ Could not save ] ')