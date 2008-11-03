import unittest
# Ensuring that the proper path is found; there must be a better way
import os
import sys
sys.path.insert(0, os.path.normpath(os.path.join(os.getcwd(), "..")))
# other imports proceed

from parsers.regex_parser import BaseParser
from src import svg

class TestBaseParser(unittest.TestCase):
    ''' description '''
    def setUp(self):
        self.p = BaseParser()

    def test__init__(self):
        self.assertEqual(self.p.directive_name, 'regex_parser')

    def test_get_svg_defs(self):
        '''get_svg_defs is really a dummy function; the test is just here
           so as to ensure there are no major changes done inadvertentdly'''
        self.assertEqual(str(self.p.get_svg_defs)[0], "<")

    def test_parse_single_line(self):
        pass
if __name__ == '__main__':
    unittest.main()