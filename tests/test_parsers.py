import unittest
import os

from mtgproxy.parsers import FileParser
from mtgproxy.models import CardMatch

TEST_DIR = os.path.join(os.path.dirname(__file__))


class TestCreateCardMatch(unittest.TestCase):
    def setUp(self):
        self.pr = FileParser()

    def test_simple_line(self):
        line = '1 Opt'
        cm = self.pr._create_card_match(line)
        self.assertIsInstance(cm, CardMatch)
        self.assertEqual(cm.name, 'Opt')
        self.assertEqual(cm.edition, '')
        self.assertEqual(cm.quantity, 1)

    def test_edition_line(self):
        line = '4 [AER] Fatal push'
        cm = self.pr._create_card_match(line)
        self.assertIsInstance(cm, CardMatch)
        self.assertEqual(cm.name, 'Fatal push')
        self.assertEqual(cm.edition, 'AER')
        self.assertEqual(cm.quantity, 4)

    def test_wrong_line_format(self):
        line = '2Fatal push'
        cm = self.pr._create_card_match(line)
        self.assertIsNone(cm)

    def test_wrong_quantity_zero(self):
        line = '0 Fatal push'
        cm = self.pr._create_card_match(line)
        self.assertIsNone(cm)

    def test_wrong_quantity_negative(self):
        line = '-1 Fatal push'
        cm = self.pr._create_card_match(line)
        self.assertIsNone(cm)

    def test_complete_file(self):
        file = os.path.join(TEST_DIR, 'fixture', 'Proxy.txt')
        card_collection = self.pr.read(file)
        self.assertEqual(card_collection[0].quantity, 1)
        self.assertEqual(card_collection[0].edition, '')
        self.assertEqual(card_collection[0].name, 'Opt')
        self.assertEqual(card_collection[1].quantity, 4)
        self.assertEqual(card_collection[1].edition, 'AER')
        self.assertEqual(card_collection[1].name, 'Fatal push')
        self.assertEqual(card_collection[2].quantity, 1)
        self.assertEqual(card_collection[2].edition, '')
        self.assertEqual(card_collection[2].name, 'oeaif')
        self.assertEqual(len(card_collection), 3)


# TODO : test custom regex
