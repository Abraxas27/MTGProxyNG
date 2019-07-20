import re
from .models import CardMatch


class FileParser:
    INPUT_REGEX = "^(?:SB\s?\:*\s?)?(\d+)\s+(?:\[(.{2}.?)\])?\s?([\w,'\-\s\(\)\./]*?)(?:\s*#+.*)?$"

    def __init__(self, custom_regex=INPUT_REGEX):
        self.regex = custom_regex
        self.pattern = re.compile(self.regex)

    def _create_card_match(self, line):
        if self.pattern.match(line):
            quantity, edition, name = [x.strip() for x in self.pattern.findall(line)[0]]
            try:
                cm = CardMatch(quantity, name, edition)
            except ValueError:
                return
            return cm
        else:
            return

    def read(self, input_file):
        card_match_collection = []
        self.pattern = re.compile(self.regex)
        with open(input_file, 'r', encoding='utf-8') as fd:
            for line in fd.readlines():
                cm = self._create_card_match(line)
                if cm:
                    card_match_collection.append(cm)
        return card_match_collection
