'''  Parser for the web_sequence diagrams
http://www.websequencediagrams.com
directive
'''

import re
from regex_parser import BaseParser
import src.svg as svg

def register_docpicture_parser(register_parser):
    register_parser(WebSequence)
    register_parser(WebSequenceEarth)
    register_parser(WebSequenceModernBlue)
    register_parser(WebSequenceMscgen)
    register_parser(WebSequenceOmegapple)
    register_parser(WebSequenceQsd)
    register_parser(WebSequenceRose)
    register_parser(WebSequenceRoundgreen)
    register_parser(WebSequenceNapkin)

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

class WebSequenceEarth(WebSequence):
    '''a parser creating web sequence diagrams; earth style'''
    def __init__(self):
        self.directive_name = 'uml_sequence:earth'
        self.style = "earth"

class WebSequenceModernBlue(WebSequence):
    '''a parser creating web sequence diagrams; modern-blue style'''
    def __init__(self):
        self.directive_name = 'uml_sequence:modern-blue'
        self.style = "modern-blue"

class WebSequenceMscgen(WebSequence):
    '''a parser creating web sequence diagrams; mscgen style'''
    def __init__(self):
        self.directive_name = 'uml_sequence:mscgen'
        self.style = "mscgen"

class WebSequenceOmegapple(WebSequence):
    '''a parser creating web sequence diagrams; omegapple style'''
    def __init__(self):
        self.directive_name = 'uml_sequence:omegapple'
        self.style = "omegapple"

class WebSequenceQsd(WebSequence):
    '''a parser creating web sequence diagrams; qsd style'''
    def __init__(self):
        self.directive_name = 'uml_sequence:qsd'
        self.style = "qsd"

class WebSequenceRose(WebSequence):
    '''a parser creating web sequence diagrams; rose style'''
    def __init__(self):
        self.directive_name = 'uml_sequence:rose'
        self.style = "rose"

class WebSequenceRoundgreen(WebSequence):
    '''a parser creating web sequence diagrams; roundgreen style'''
    def __init__(self):
        self.directive_name = 'uml_sequence:roundgreen'
        self.style = "roundgreen"

class WebSequenceNapkin(WebSequence):
    '''a parser creating web sequence diagrams; napkin style'''
    def __init__(self):
        self.directive_name = 'uml_sequence:napkin'
        self.style = "napkin"
