'''  Silly example

This is a rather silly example showing the potential power of docpicture,
but also highlighting some safety issue.

This file is not in the parser directory.  Therefore, it is not recognized
by docpicture as a valid parser when it is started.  However, in the demo,
we set the directive to be trusted which allows it to proceed.  The way
it does so is by performing "exec" on the code included in the page.
The final result will be seen, provided you have matplotlib installed.

..docpicture:: unsafe_matplotlib
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import matplotlib.mlab as mlab
    from pylab import rand

    mpl.rcParams['xtick.labelsize'] = 10
    mpl.rcParams['ytick.labelsize'] = 12
    mpl.rcParams['axes.edgecolor'] = 'gray'

    global fig
    fig = plt.figure()

    def add_math_background():
        ax = fig.add_axes([0., 0., 1., 1.])

        text = []
        text.append((r"$W^{3\\beta}_{\\delta_1 \\rho_1 \\sigma_2} = U^{3\\beta}_{\\delta_1 \\rho_1} + \\frac{1}{8 \\pi 2} \\int^{\\alpha_2}_{\\alpha_2} d \\alpha^\\prime_2 \\left[\\frac{ U^{2\\beta}_{\\delta_1 \\rho_1} - \\alpha^\\prime_2U^{1\\beta}_{\\rho_1 \\sigma_2} }{U^{0\\beta}_{\\rho_1 \\sigma_2}}\\right]$", (0.7, 0.2), 20))
        text.append((r"$\\frac{d\\rho}{d t} + \\rho \\vec{v}\\cdot\\nabla\\vec{v} = -\\nabla p + \\mu\\nabla^2 \\vec{v} + \\rho \\vec{g}$",
                    (0.35, 0.9), 20))
        text.append((r"$\\int_{-\\infty}^\\infty e^{-x^2}dx=\\sqrt{\\pi}$",
                    (0.15, 0.3), 25))
        #text.append((r"$E = mc^2 = \\sqrt{{m_0}^2c^4 + p^2c^2}$",
        #            (0.7, 0.42), 30))
        text.append((r"$F_G = G\\frac{m_1m_2}{r^2}$",
                    (0.85, 0.7), 30))
        for eq, (x, y), size in text:
            ax.text(x, y, eq, ha='center', va='center', color="#11557c", alpha=0.25,
                    transform=ax.transAxes, fontsize=size)
        ax.set_axis_off()
        return ax

    def add_matplotlib_text(ax):
        ax.text(0.95, 0.5, 'matplotlib', color='#11557c', fontsize=65,
                   ha='right', va='center', alpha=1.0, transform=ax.transAxes)

    def add_polar_bar():
        global np, cm
        ax = fig.add_axes([0.025, 0.075, 0.2, 0.85], polar=True)
        ax.axesPatch.set_alpha(0.05)
        ax.set_axisbelow(True)
        N = 7
        arc = 2. * np.pi
        theta = np.arange(0.0, arc, arc/N)
        radii = 10 * np.array([0.2, 0.6, 0.8, 0.7, 0.4, 0.5, 0.8])
        width = np.pi / 4 * np.array([0.4, 0.4, 0.6, 0.8, 0.2, 0.5, 0.3])
        bars = ax.bar(theta, radii, width=width, bottom=0.0)
        for r, bar in zip(radii, bars):
            bar.set_facecolor(cm.jet(r/10.))
            bar.set_alpha(0.6)

        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_visible(False)

        for line in ax.get_ygridlines() + ax.get_xgridlines():
            line.set_lw(0.8)
            line.set_alpha(0.9)
            line.set_ls('-')
            line.set_color('0.5')

        ax.set_yticks(np.arange(1, 9, 2))
        ax.set_rmax(9)

    main_axes = add_math_background()
    add_polar_bar()
    add_matplotlib_text(main_axes)

'''
from StringIO import StringIO

from parsers.regex_parser import BaseParser
import src.svg as svg


matplotlib_included = True
try:
    import matplotlib
    matplotlib.use('SVG')
    from matplotlib import pyplot
except:
    matplotlib_included = False


def register_docpicture_parser(register_parser):
    register_parser(Plot)

class Plot(BaseParser):
    '''a parser creating web sequence diagrams'''
    def __init__(self):
        self.directive_name = 'unsafe_matplotlib'

    def create_picture(self, lines):
        '''Parses all received lines of code, and exec the result
        '''
        if not matplotlib_included:
            text = "A recent version of matplotlib is needed for this example."
            warning = svg.XmlElement("pre", text=text)
            warning.attributes["class"] = "warning"
            return warning
        full_length = len(lines[0])
        reduced_length = len(lines[0].lstrip())
        indentation = full_length - reduced_length

        code_lines = []
        for line in lines:
            if line.strip == "":
                continue
            code_lines.append(line[indentation:])
        complete_code = '\n'.join(code_lines)
        exec complete_code

        temp_file = StringIO()
        fig.savefig(temp_file)
        content = temp_file.getvalue()
        temp_file.close()
        lines = content.split("\n")
        content = '\n'.join(lines[4:])
        return content