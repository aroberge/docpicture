import unittest
# Ensuring that the proper path is found; there must be a better way
import os
import sys
sys.path.insert(0, os.path.normpath(os.path.join(os.getcwd(), "..")))
# other imports proceed

from parsers.regex_parser import BaseParser

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

    def test_parsing_error(self):
        lines = ["Dummy1", "Dummy2"]
        self.assert_("Error" in str(self.p.parsing_error(lines)))
        self.assert_("warning" in str(self.p.parsing_error(lines)))
        self.assert_("Dummy1" in str(self.p.parsing_error(lines)))
        self.assert_("Dummy2" in str(self.p.parsing_error(lines)))

    def test_draw_picture(self):
        lines = ["Dummy1", "Dummy2"]
        self.assert_("Drawing" in str(self.p.draw_picture(lines)))
        for line in lines:
            self.assert_(line in str(self.p.draw_picture(lines)))

    def test_create_picture(self):
        good_lines = ["This is good", "More good stuff", "All goodness"]
        self.assert_("Drawing" in str(self.p.create_picture(good_lines)))
        for line in good_lines:
            self.assert_(str(("good", ())) in
                                    str(self.p.create_picture(good_lines)))
        bad_lines = good_lines[:]
        bad_lines.insert(2, "A bad line")
        self.assert_("Error" in str(self.p.create_picture(bad_lines)))
        self.assert_("A bad line" in str(self.p.create_picture(bad_lines)))
        self.assert_("good" not in str(self.p.create_picture(bad_lines)))

if __name__ == '__main__':
    unittest.main()