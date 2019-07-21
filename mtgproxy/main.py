import os
import glob

import time

from mtgproxy.harvesters import DirectoryHarvester, ScryfallHarvester
from mtgproxy.parsers import FileParser
from mtgproxy.pdf import print_pdf

ROOT_DIR = os.path.join(os.getcwd(), '..')
SCANS_DIR = os.path.join(ROOT_DIR, 'tests/fixture/scans')

if __name__ == '__main__':
    files = glob.glob(os.path.join(ROOT_DIR, 'temp', '*'))
    for f in files:
        os.remove(f)
    # On lit la liste et on extrait les cartes demandées et leur quantité
    card_collection = FileParser().read(os.path.join(ROOT_DIR, 'tests/fixture/Proxy.txt'))
    # print(card_collection)
    # On crée la classe de recherche des scans
    h = ScryfallHarvester()
    # h = DirectoryHarvester(SCANS_DIR)
    filenames = []
    # Pour chaque carte recherchée
    for cardmatch in card_collection:
        # On récupère le chemin des fichiers de la face et du dos
        # front, back = es.get_scan(cardmatch)
        start = time.time()
        front = h.get_scan(cardmatch)
        end = time.time()
        print('Carte {} récupérée en {:.3f} secondes'.format(cardmatch.name, end - start))
        # Pour le nombre d'occurences demandé...
        for i in range(0, cardmatch.quantity):
            # ...on ajoute la face de la carte...
            if front:
                filenames.append(front)
            # ...et le dos s'il existe
            # if back:
            #     filenames.append(back)
    # print(filenames)
    start = time.time()
    print_pdf(os.path.join(ROOT_DIR, 'temp', 'proxy.pdf'), filenames)
    end = time.time()
    print('PDF généré en {:.3f} secondes'.format(end - start))
