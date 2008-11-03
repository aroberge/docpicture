'''
This module contains the base regex_parser class from which all
regular expression based parsers could be derived.
Some methods are implemented only to provide testing, and
are meant to be overriden.
'''

import re
import src.svg as svg

''' So as to make the parser classes more readable, we suggest that
statement patterns, if using the re module, or the grammar definition,
if using some other module, as well as svg "defs" be defined first,
before the class definition.'''

# To enable testing, we define at least one pattern to match.
_patterns = {
    # anything with "good" in it is declared to be good ;-)
    'good': re.compile(".*good.*")
}

class BaseParser(object):
    '''Base class for all the parsers'''
    def __init__(self):
        self.patterns = _patterns
        self.directive_name = 'regex_parser'

    def get_svg_defs(self):
        '''returns default svg_defs; normally overriden by parsers'''
        defs = svg.SvgDefs()
        defs.append(svg.Comment("For testing purpose."))
        return defs

    def parse_single_line(self, line):
        '''Parses a given line to see if it match a known pattern'''
        line = line.strip()
        for name in self.patterns:
            result = self.patterns[name].match(line)
            if result is not None:
                return name, result.groups()
        return None, line

    def parsing_error(self, lines):
        '''this function can be replaced by a custom one.'''
        lines.insert(0, 'Error: the following lines are not parsed properly.')
        pre = svg.XmlElement("pre", text = '\n'.join(lines))
        pre.attributes['class'] = 'warning'  # defined in main program
        return pre

    def draw_picture(self, lines):
        '''this function is meant to be replaced by a custom one.'''
        result = ["Drawing goes here:"]
        for line in lines:
            result.append(str(line))
        return svg.XmlElement("pre", text = '\n'.join(result))

    def create_picture(self, lines):
        '''Parses all received lines of code and return the result of
        the appropriate method, based on whether or not errors were found.
        
        If errors are found, lines with errors are passed to parsing error
        as a list; otherwise, regex parsing results are passed to draw_picture
        as a list.  A parser subclassing BaseParser needs to implement
        draw_picture and may rely on the default for parsing error.
        '''
        ok_lines = []
        problem_lines = []
        for line in lines:
            if line.strip() == "":
                continue
            result = self.parse_single_line(line)
            if result[0] == None:
                problem_lines.append(line)
            else:
                ok_lines.append(result)
        if problem_lines:
            return self.parsing_error(problem_lines)
        else:
            return self.draw_picture(ok_lines)

