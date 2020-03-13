import os

from scripts.common import Json
from scripts.links import MedsLinksExtractor
from scripts.med import MedInfoExtractor
from scripts.lab import LabInfoExtractor

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MED_LINKS_DB = os.path.join(BASE_DIR, 'data', 'links.json')
MED_INFOS_DB = os.path.join(BASE_DIR, 'data', 'meds.json')


if __name__ == "__main__":
    print('Extracting Links')
    meds_links = MedsLinksExtractor.extract(save_path = MED_LINKS_DB)

    print('Extracting Meds')
    meds = {letter : [] for letter in MedsLinksExtractor.letters}
    for letter, links in meds_links.items():
        for i, link in enumerate(links):
            try:
                print('Letter {} | Med [{:2}/{:2}]'.format(letter, i, len(links)), end = "\r")
                tmp = MedInfoExtractor.scrap_med_page(link)
                if tmp:
                    meds[letter] += [tmp]
            except Exception as e:
                print(link)
        Json.save(MED_INFOS_DB, meds)
        print('Saving {}'.format(letter))

    # meds = Json.read(MED_INFOS_DB)

    print('Extracting Labs')
    for letter, letter_meds in meds.items():
        for i, med in enumerate(letter_meds):
            print('Letter {} | Med Lab [{:2}/{:2}]'.format(letter, i, len(letter_meds)), end = "\r")
            if 'lab' in med and 'img' not in med['lab']:
                LabInfoExtractor.extract(med['lab'])
                Json.save(MED_INFOS_DB, meds)