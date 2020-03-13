import os

from scripts.links import MedsLinksExtractor
from scripts.meds import MedInfoExtractor
from scripts.common import Json

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MED_LINKS_DB = os.path.join(BASE_DIR, 'data', 'links.json')
MED_INFOS_DB = os.path.join(BASE_DIR, 'data', 'meds.json')
LABS_DB = os.path.join(BASE_DIR, 'data', 'labs.json')


if __name__ == "__main__":
    print('Extracting Links')
    meds_links = MedsLinksExtractor.extract(save_path = MED_LINKS_DB)

    print('Extracting Meds')
    meds = {letter : [] for letter in MedsLinksExtractor.letters}
    for letter, links in meds_links.items():
        for i, link in enumerate(links):
            print('Letter {} | Med [{:2}/{:2}]'.format(letter, i, len(links)), end = "\r")
            meds[letter] += [MedInfoExtractor.scrap_med_page(link)]
            Json.save(MED_INFOS_DB, meds)


    print('Extracting Labs')
    labs = []
    for letter, letter_meds in meds.items():
        for i, med in enumerate(letter_meds):
            print('Letter {} | Med [{:2}/{:2}]'.format(letter, i, len(letter_meds)), end = "\r")
            if 'lab' in med:
                labs += [med['lab']]
                Json.save(LABS_DB, labs)
    