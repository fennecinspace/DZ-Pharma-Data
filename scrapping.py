# -*- coding: utf-8 -*-
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
import sys, json
import re

links = [
    'https://pharmnet-dz.com/alphabet.aspx?char=A',
    'https://pharmnet-dz.com/alphabet.aspx?char=B',
    'https://pharmnet-dz.com/alphabet.aspx?char=C',
    'https://pharmnet-dz.com/alphabet.aspx?char=D',
    'https://pharmnet-dz.com/alphabet.aspx?char=E',
    'https://pharmnet-dz.com/alphabet.aspx?char=F',
    'https://pharmnet-dz.com/alphabet.aspx?char=G',
    'https://pharmnet-dz.com/alphabet.aspx?char=H',
    'https://pharmnet-dz.com/alphabet.aspx?char=I',
    'https://pharmnet-dz.com/alphabet.aspx?char=J',
    'https://pharmnet-dz.com/alphabet.aspx?char=K',
    'https://pharmnet-dz.com/alphabet.aspx?char=L',
    'https://pharmnet-dz.com/alphabet.aspx?char=M',
    'https://pharmnet-dz.com/alphabet.aspx?char=N',
    'https://pharmnet-dz.com/alphabet.aspx?char=O',
    'https://pharmnet-dz.com/alphabet.aspx?char=P',
    'https://pharmnet-dz.com/alphabet.aspx?char=Q',
    'https://pharmnet-dz.com/alphabet.aspx?char=R',
    'https://pharmnet-dz.com/alphabet.aspx?char=S',
    'https://pharmnet-dz.com/alphabet.aspx?char=T',
    'https://pharmnet-dz.com/alphabet.aspx?char=U',
    'https://pharmnet-dz.com/alphabet.aspx?char=V',
    'https://pharmnet-dz.com/alphabet.aspx?char=W',
    'https://pharmnet-dz.com/alphabet.aspx?char=X',
    'https://pharmnet-dz.com/alphabet.aspx?char=Y',
    'https://pharmnet-dz.com/alphabet.aspx?char=Z',
]

meds_links = {}
meds = {}
nb_total_meds = 0
nb_processing_dotes = 0
SITE_URL = "https://pharmnet-dz.com/"

print("-------------------------------------")
## going through letters
for index, link in enumerate(links):
    char_page = urlopen(link)
    soup = BeautifulSoup(char_page, "html5lib")
    nb_pages = len(soup.find_all('a', class_ ="btn btn-xs btn-warning")) + len(soup.find_all('a', class_ = "btn btn-danger"))
    meds_links[link[-1]] = []
    meds[link[-1]] = []
    print('Letter : ' + str(link[-1]) + ' / Pages : '+ str(nb_pages))

    ## going through pages
    for i in range(1, nb_pages + 1):
        page_to_scrap = BeautifulSoup(urlopen(link + '&p=' + str(i)), "html5lib")
        all_meds = page_to_scrap.find_all(attrs={'scope':'row'})

        ## going through drugs and scrapping data
        for y, med in enumerate(all_meds):
            try:
                if nb_processing_dotes < 3:
                    nb_processing_dotes += 1
                else:
                    nb_processing_dotes = 1

                print('\rProcessing -> Page ' + str(i) + " Med " + str(y + 1) + "." * nb_processing_dotes + "   " , end='')
                elem = {} 
                
                ## getting and encoding site url
                med_link = med.find_all('a')[0]['href']
                med_url = SITE_URL + quote(med_link)

                ## opening med page
                page_to_bs4 = urlopen(med_url)
                med_page = BeautifulSoup( page_to_bs4.read().decode('utf-8'), "html5lib")
                left_info = med_page.find('div', class_ ='col-lg-7 col-md-7 col-sm-8 col-xs-12')
                right_info = med_page.find('div', class_ ='col-lg-5 col-md-5 col-sm-4 col-xs-12')

                ## getting headline name
                tmp = med_page.find(attrs={'style' : 'text-shadow: 3px 3px rgb(216, 228, 237); padding-left: 10px; padding-right: 10px; margin-top:0px;'})
                if tmp:
                    elem['Nom'] = tmp.text

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
                for line in all_lines:
                    if 'Liste' in line:
                        if len(line) > 40:
                            elem['Liste'] = line[35:]
                    if 'Pays' in line:
                        if len(line) > 34:
                            elem['Pays'] = line[34:]
                    if 'Tarif' in line:
                        if len(line) > 50:
                            elem['Tarif de reference'] = line[48:]
                    if 'PPA' in line:
                        if len(line) > 46:
                            elem['PPA'] = line[46:]
                    if 'Enregistrement' in line:
                        if len(line) > 48:
                            elem['Num Enregistrement'] = line[48:]
                    if 'Commercial' in line:
                        if len(line) > 44:
                            elem['Nom Commercial'] = line[44:]
                    if 'Code' in line:
                        if len(line) > 38:
                            elem['Code DCI'] = line[38:]
                    if 'Forme' in line:
                        if len(line) > 35:
                            elem['Forme'] = line[35:]
                    if 'Dosage' in line:
                        if len(line) > 36:
                            elem['Dosage'] = line[36:]
                    if 'Conditionnement' in line:
                        if len(line) > 45:
                            elem['Conditionnement'] = line[45:]

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
                
                # print(elem)    
                ## saving page link
                meds_links[link[-1]] += [med_url]
                ## saving page data
                meds[link[-1]] += [elem]
            except Exception as e:
                print('\n', e)
                continue

    nb_meds = len(meds[link[-1]])
    nb_total_meds += nb_meds
    print("\rNumber of Meds : {}                    ".format(nb_meds))
    print("-------------------------------------")

print("\rTotal Number of Meds : {}                    ".format(nb_total_meds))
## saving data
try:
    with open('links.json', 'w') as fp:
        json.dump(meds_links, fp)
except Exception as e:
    print(e)

try:
    with open('result.json', 'w') as fp:
        json.dump(meds, fp)
except Exception as e:
    print(e)