'''  Parser for creating mathematical equations.
'''

import re
from regex_parser import BaseParser
import src.svg as svg
from StringIO import StringIO

matplotlib_included = True
try:
    import matplotlib
    matplotlib.use('SVG')
    from matplotlib import pyplot
except:
    matplotlib_included = False


def register_docpicture_parser(register_parser):
    register_parser(Equations)

class Equations(BaseParser):
    '''a parser creating web sequence diagrams'''
    def __init__(self):
        self.directive_name = 'equation'

    def get_svg_defs(self):
        '''No svg diagrams produced by this parser.'''
        return svg.Comment("ignore me")

    def create_picture(self, lines):
        '''Parses all received lines of code.

           We assume that all lines are meant to be a single line equation
        '''
        if not matplotlib_included:
            text = "A recent version of matplotlib is needed for this example."
            warning = svg.XmlElement("pre", text=text)
            warning.attributes["class"] = "warning"
            return warning
        equation = ' '.join(lines)
        fig = pyplot.figure()
        fig.set_size_inches(8, 1)

        ax = fig.add_axes([0., 0., 1.0, 1.0])
        ax.set_axis_off()
        ax.text(0, 0, r"$%s$"%equation, color='#11557c', fontsize=25)

        temp_file = StringIO()
        fig.savefig(temp_file)
        content = temp_file.getvalue()
        temp_file.close()
        lines = content.split("\n")
        content = '\n'.join(lines[4:])
        return content