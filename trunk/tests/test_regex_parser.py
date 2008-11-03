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
        self.assertEqual(self.p.parse_single_line(" this is good"), ("good", ()))
        self.assertEqual(self.p.parse_single_line("this is bad"), (None, "this is bad"))

    def test_draw_warning(self):
        lines = ["Dummy1", "Dummy2"]
        self.assert_("Warning" in str(self.p.draw_warning(lines)))
        self.assert_("Dummy" in str(self.p.draw_warning(lines)))

    def test_create_picture(self):
        good_lines = ["This is good", "More good stuff", "All goodness"]
        self.assert_("Drawing" in str(self.p.create_picture(good_lines)))

if __name__ == '__main__':
    unittest.main()