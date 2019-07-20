import os
import glob

from mtgproxy.harvesters import DirectoryHarvester, ScryfallHarvester
from mtgproxy.parsers import FileParser

ROOT_DIR = os.path.join(os.getcwd(), '..')
SCANS_DIR = os.path.join(ROOT_DIR, 'tests/fixture/scans')

if __name__ == '__main__':
    files = glob.glob(os.path.join(ROOT_DIR, 'temp', '*'))
    for f in files:
        os.remove(f)
    # On lit la liste et on extrait les cartes demandées et leur quantité
    card_collection = FileParser().read(os.path.join(ROOT_DIR, 'tests/fixture/Proxy.txt'))
    print(card_collection)
    # On crée la classe de recherche des scans
    h = ScryfallHarvester()
    # h = DirectoryHarvester(SCANS_DIR)
    filenames = []
    # Pour chaque carte recherchée
    for cardmatch in card_collection:
        # On récupère le chemin des fichiers de la face et du dos
        # front, back = es.get_scan(cardmatch)
        front = h.get_scan(cardmatch)
        # Pour le nombre d'occurences demandé...
        for i in range(0, cardmatch.quantity):
            # ...on ajoute la face de la carte...
            if front:
                filenames.append(front)
            # ...et le dos s'il existe
            # if back:
            #     filenames.append(back)
    # On affiche la liste des fichiers à faire figurer sur la planche finale
    print(filenames)
