import unittest
import os

from mtgproxy.harvesters import DirectoryHarvester
from mtgproxy.models import CardMatch

TEST_SCANS_DIR = os.path.join(os.path.dirname(__file__), 'fixture', 'scans')


class TestDirectoryHarvester(unittest.TestCase):
    def setUp(self):
        self.dh = DirectoryHarvester('../tests/fixture/scans', edition_types=['core', 'expansion'])

    def test_scan_from_latest_edition(self):
        cm = CardMatch(1, 'opt')
        self.assertEqual(self.dh.get_scan(cm), os.path.join(TEST_SCANS_DIR, 'M19', 'opt.jpg'))

    def test_scan_cases_insensitive(self):
        cm = CardMatch(1, 'fatal push')
        self.assertEqual(self.dh.get_scan(cm), os.path.join(TEST_SCANS_DIR, 'AER', 'Fatal Push.jpg'))

    def test_scan_not_found(self):
        cm = CardMatch(1, 'Leyline of the Void')
        self.assertIsNone(self.dh.get_scan(cm))

    def test_scan_from_specific_edition(self):
        cm = CardMatch(1, 'Opt', edition='DOM')
        self.assertEqual(self.dh.get_scan(cm), os.path.join(TEST_SCANS_DIR, 'DOM', 'Opt.jpg'))

    def test_scan_not_found_specific_edition(self):
        cm = CardMatch(1, 'Fatal Push', edition='DOM')
        self.assertIsNone(self.dh.get_scan(cm))

# TODO : unit test ScryfallHarvester