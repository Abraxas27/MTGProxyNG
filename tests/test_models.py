import unittest

from mtgproxy.parsers import FileParser
from mtgproxy.models import CardMatch


class TestCreateCardMatch(unittest.TestCase):
    def test_simple_line(self):
        pr = FileParser()
        line = '1 Opt'
        cm = pr._create_card_match(line)
        self.assertIsInstance(cm, CardMatch)
        self.assertEqual(cm.name, 'Opt')
        self.assertEqual(cm.edition, '')
        self.assertEqual(cm.quantity, 1)

    def test_edition_line(self):
        pr = FileParser()
        line = '4 [AER] Fatal push'
        cm = pr._create_card_match(line)
        self.assertIsInstance(cm, CardMatch)
        self.assertEqual(cm.name, 'Fatal push')
        self.assertEqual(cm.edition, 'AER')
        self.assertEqual(cm.quantity, 4)

    def test_wrong_line_format(self):
        pr = FileParser()
        line = '2Fatal push'
        cm = pr._create_card_match(line)
        self.assertIsNone(cm)

    def test_wrong_quantity_zero(self):
        pr = FileParser()
        line = '0 Fatal push'
        cm = pr._create_card_match(line)
        self.assertIsNone(cm)

    def test_wrong_quantity_negative(self):
        pr = FileParser()
        line = '-1 Fatal push'
        cm = pr._create_card_match(line)
        self.assertIsNone(cm)
