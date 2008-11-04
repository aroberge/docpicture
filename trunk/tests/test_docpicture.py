

import unittest
import re

# Ensuring that the proper path is found; there must be a better way
import os
import sys
current_path = os.path.normpath(os.path.join(os.path.realpath(__file__), ".."))
sys.path.insert(0, os.path.normpath(os.path.join(current_path, "..")))

import docpicture
from parsers.regex_parser import BaseParser
from src import svg

class FakeParser(BaseParser):
    def __init__(self):
        self.directive_name = 'good'
        self.patterns = {
        # anything with "good" in it is declared to be good ;-)
        # however, no information is retained.
        'good': re.compile(".*good.*")
        }
    def create_drawing(self, lines):
        new_lines = [str(line) for line in lines]
        text = "\n".join(new_lines)
        pre = svg.XmlElement("pre", text=text)
        pre.attributes["class"] = "fake_drawing"
        return pre

def find_me():
    '''Just a test function.'''
    pass

def register_docpicture_parser(register_parser):
    '''for testing'''
    register_parser(FakeParser)


class TestDocpictureDocument(unittest.TestCase):

    def setUp(self):
        # an instance with no parser defined
        self.no = docpicture.DocpictureDocument(obj=find_me)
        # an instance with a parser defined
        self.fake = FakeParser()
        self.yes = docpicture.DocpictureDocument(parsers = {'good': self.fake},
                                                 obj=self.fake)
        return

    def test_is_docpicture_directive(self):
        self.assert_(not self.no.is_docpicture_directive("a string"))
        self.assert_(self.yes.indentation == None)
        self.assert_(self.yes.current_parser_name == None)
        self.assert_(not self.yes.is_docpicture_directive("a good string"))

        self.assert_(self.yes.is_docpicture_directive("  ..docpicture:: good"))
        self.assert_(self.yes.indentation == 2)
        self.assert_(self.yes.current_parser_name == 'good')

        self.assert_(not self.yes.is_docpicture_directive("..docpicture:: unknown"))

    def test_retrieve_docpicture_parser(self):
        self.assert_(isinstance(self.yes.retrieve_docpicture_parser('good'),
                                FakeParser))
        self.assert_(not self.yes.retrieve_docpicture_parser('unknown'))
        self.assert_(not self.no.retrieve_docpicture_parser('good'))

    def test_is_docpicture_code(self):
        self.assert_(self.yes.current_parser_name == None)
        self.assert_(self.yes.indentation == None)
        self.assert_(self.yes.is_docpicture_code("    "))
        self.yes.indentation = 1
        self.assert_(self.yes.is_docpicture_code("  test"))
        self.assert_(self.yes.is_docpicture_code("     test"))
        self.assert_(self.yes.is_docpicture_code(""))
        self.assert_(self.yes.is_docpicture_code("    \t"))
        self.assert_(not self.yes.is_docpicture_code(" test"))
        self.assert_(not self.yes.is_docpicture_code("test"))

    def test_process_docpicture_code(self):
        some_bad_lines = ["  good line", "  this is a bad line", " good",
                          "not", "good"]
        all_good_lines = ["  good line", "goodness", "very good indeed"]
        self.yes.current_parser_name = 'good'

        bad_output = str(self.yes.process_docpicture_code(some_bad_lines)).strip()
        good_output = str(self.yes.process_docpicture_code(all_good_lines)).strip()

        bad_ = """<pre class="warning">Error: the following lines are not parsed properly.
  this is a bad line
not</pre>"""
        good_ = """<pre>Drawing goes here:
('good', ())
('good', ())
('good', ())</pre>"""

        self.assert_(bad_output == bad_)
        self.assert_(good_output == good_)

    def test_embed_docpicture_code(self):

        some_bad_lines = ["  ..docpicture:: good", "  this is a bad line",
                          " good", "not", "good"]
        all_good_lines = ["  ..docpicture:: good", "goodness",
                          "very good indeed"]
        self.yes.current_parser_name = 'good'
        self.yes.body = svg.XmlElement("body")
        self.yes.embed_docpicture_code(some_bad_lines)
        # the first time we run the test, we expect the svg defs to be included
        # before the code. Note that only 2 "good lines" are included in the
        # drawing, as the first line with "good" in it is the docpicture
        # directive, which is expected to be excluded.
        expected_output = """<body>
    <pre class="docpicture">  ..docpicture:: good
  this is a bad line
 good
not
good</pre>
    <svg:svg width="0" height="0">
    <svg:defs>
  <!-- For testing purpose. -->
</svg:defs>
</svg:svg>
    <pre class="warning">Error: the following lines are not parsed properly.
  this is a bad line
not</pre>
</body>"""
        self.assert_(str(self.yes.body).strip() == expected_output)

        self.yes.body = svg.XmlElement("body")
        self.yes.embed_docpicture_code(all_good_lines)
        # the second time we run a different test, the svg defs do not need to
        # be included.
        expected_output = """<body>
    <pre class="docpicture">  ..docpicture:: good
goodness
very good indeed</pre>
    <pre>Drawing goes here:
('good', ())
('good', ())</pre>
</body>"""
        self.assert_(str(self.yes.body).strip() == expected_output)
        return

    def test_process_lines_of_text(self):
        lines = [line.replace("\n", '') for line in
                 open(os.path.join(current_path, "test_document_in.txt")
                                                                ).readlines()]
        self.yes.body = svg.XmlElement("body")
        self.yes.process_lines_of_text(lines)
        expected_output = open(os.path.join(current_path,
                                            "test_document_out.txt")).read()
        self.assert_(expected_output == str(self.yes.body).strip())
        return

    def test_create_document(self):
        text = open(os.path.join(current_path, "test_document_in.txt")).read()
        self.yes.create_document(text)
        self.yes.head.append(svg.XmlElement("style",
                                            text=".fake_drawing{color:green;}"))
        expected_output = open(os.path.join(current_path,
                                            "test_document_out.xml")).read()
        self.assert_(expected_output == str(self.yes.document).strip())
        return

    def test_find_object(self):
        self.assert_(not self.no.find_object('unknown'))
        self.assert_(self.no.find_object('find_me')==find_me)
        self.assert_(self.no.find_object('FakeParser')==FakeParser)
        self.assert_(not self.yes.find_object('unknown'))
        self.assert_(self.yes.find_object('find_me')==find_me)
        self.assert_(self.yes.find_object('FakeParser')==FakeParser)


if __name__ == '__main__':
    unittest.main()