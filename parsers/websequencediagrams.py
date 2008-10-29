'''  Parser for the web_sequence diagrams
http://www.websequencediagrams.com
directive
'''

import re
from _parser import BaseParser
import src.svg as svg

def register_docpicture_parser(register_parser):
    register_parser(WebSequence)

class WebSequence(BaseParser):
    '''a parser creating web sequence diagrams'''
    def __init__(self):
        self.directive_name = 'uml_sequence'
        self.style = "default"

    def get_svg_defs(self):
        '''No svg diagrams produced by this parser.'''
        return svg.Comment("ignore me")

    def create_drawing(self, lines):
        '''Parses all received lines of code.

           NORMALLY, If errors are found, returns a list of line with errors and
           an empty string, otherwise returns None (for no error) and a list of
           lines parsed to extract the relevant information.

           HOWEVER, here we assume that all lines are valid lines as they are
           passed to a remote server which should deal with them...
        '''
        div = svg.XmlElement("div", wsd_style=self.style)
        div.attributes['class'] = "wsd"
        text = "\n".join(lines)
        div.append(svg.XmlElement("pre", text=text))
        main_div = svg.XmlElement("div")
        main_div.append(div)
        main_div.append(svg.XmlElement("script",
                            type="text/javascript",
                            src="http://www.websequencediagrams.com/service.js"))
        return None, main_div

class WebSequenceEarth(Websequence):
    '''a parser creating web sequence diagrams; earth style'''
    def __init__(self):
        self.directive_name = 'uml_sequence:earth'
        self.style = "earth"

class WebSequenceModernBlue(Websequence):
    '''a parser creating web sequence diagrams; modern-blue style'''
    def __init__(self):
        self.directive_name = 'uml_sequence:modern-blue'
        self.style = "modern-blue"

class WebSequenceMscgen(Websequence):
    '''a parser creating web sequence diagrams; mscgen style'''
    def __init__(self):
        self.directive_name = 'uml_sequence:mscgen'
        self.style = "mscgen"

class WebSequenceOmegapple(Websequence):
    '''a parser creating web sequence diagrams; omegapple style'''
    def __init__(self):
        self.directive_name = 'uml_sequence:omegapple'
        self.style = "omegapple"

class WebSequenceQsd(Websequence):
    '''a parser creating web sequence diagrams; qsd style'''
    def __init__(self):
        self.directive_name = 'uml_sequence:qsd'
        self.style = "qsd"

class WebSequenceRose(Websequence):
    '''a parser creating web sequence diagrams; rose style'''
    def __init__(self):
        self.directive_name = 'uml_sequence:rose'
        self.style = "rose"

"""
    * default
    * earth
    * modern-blue
    * mscgen
    * omegapple
    * qsd
    * rose
    * roundgreen
    * napkin
"""