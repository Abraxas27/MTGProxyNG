import os
import json
import re
from abc import abstractmethod
import requests
import uuid

ROOT_DIR = os.path.join(os.getcwd(), '..')
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# TODO : support double-face cards ----> if card_faces in resp.keys()
class Harvester:
    def __init__(self, edition_types=None):
        self.edition_types = edition_types or ['core', 'expansion']

    @abstractmethod
    def get_scan(self, cardmatch):
        pass


class ScryfallHarvester(Harvester):
    def __init__(self, edition_types=None):
        super().__init__(edition_types=edition_types)

    def get_scan(self, cardmatch):
        payload = {'exact': cardmatch.name.lower()}
        if cardmatch.edition:
            payload['set'] = cardmatch.edition.lower()
        resp = requests.get("https://api.scryfall.com/cards/named", params=payload).json()
        try:
            if resp['object'] == 'card':
                unique_filename = os.path.join(ROOT_DIR, 'temp', str(uuid.uuid4()) + '.jpg')
                r = requests.get(resp['image_uris']['large'])
                open(unique_filename, 'wb').write(r.content)
                return unique_filename
        except KeyError:
            pass


class DirectoryHarvester(Harvester):
    def __init__(self, scans_dir, edition_types=None):
        super().__init__(edition_types=edition_types)
        self.scans_dir = scans_dir
        self.editions_order = self._sort_by_release_date()

    def _sort_by_release_date(self):
        editions = {}
        with open(os.path.join(DATA_DIR, 'SetList.json'), 'r', encoding='utf-8') as fd:
            set_list = json.load(fd)
        for e in set_list:
            if e['type'] in self.edition_types:
                k = e['code']
                editions[k] = e
        return sorted(editions.keys(), key=lambda key: re.sub('-', '', editions[key]['releaseDate']), reverse=True)

    def _find(self, cardmatch, directory=None):
        found = {}
        searched_dir = directory or self.scans_dir

        for entry in os.scandir(searched_dir):
            if entry.is_dir(follow_symlinks=False):
                found.update(self._find(cardmatch, entry.path))
            elif re.match(cardmatch.name.lower(), entry.name, re.I):
                found[os.path.basename(os.path.dirname(entry.path))] = os.path.realpath(entry.path)
        return found

    def get_scan(self, cardmatch):
        if cardmatch.edition:
            f = self._find(cardmatch, os.path.join(self.scans_dir, cardmatch.edition))
            if cardmatch.edition in f.keys():
                return f[cardmatch.edition]
            else:
                return
        else:
            f = self._find(cardmatch, os.path.join(self.scans_dir))
            for edition in self.editions_order:
                if edition in f.keys():
                    return f[edition]
            return

