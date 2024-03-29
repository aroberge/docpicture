"""
SVG renderer.

(C) 2006 Chris Liechti <cliechti@gmx.net>
"""

from xml.sax.saxutils import escape

class SVGOutputVisitor:
    """Render a list of shapes as SVG image."""
    
    def __init__(self, file_like, scale = 1, line_width=1, unit='',
                 foreground=(0,0,0), background=(255,255,255), fillcolor=(0,0,0)
        ):
        self.file_like = file_like
        self.scale = scale
        self.unit = unit
        self.line_width = line_width
        self.foreground = foreground
        self.background = background
        self.fillcolor = fillcolor
        self.indent = ''
    
    def _num(self, number):
        """helper to format numbers with scale and unit for svg output"""
        return "%d%s" % (number*self.scale, self.unit)

    def _unit(self, number):
        """helper to format numbers with unit for svg output"""
        return "%d%s" % (number, self.unit)

    def _color(self, color):
        r,g,b = color
        return '#%02x%02x%02x' % (r,g,b)
    
    def get_size_attrs(self):
        """get image size as svg text"""
        #this function is here beacuse of a hack. the rst2html converter
        #has to know the size of the figure it inserts
        return 'width="%s" height="%s"' % (
            self._num(self.width),
            self._num(self.height)
        )
    
    def visit_image(self, aa_image, xml_header=True):
        """Process the given ASCIIArtFigure and output the shapes in
           the SVG file
        """
        self.aa_image = aa_image        #save for later XXX not optimal to do it here
        self.width = (aa_image.width+1)*aa_image.nominal_size*aa_image.aspect_ratio
        self.height = (aa_image.height+1)*aa_image.nominal_size
        if xml_header:
            self.file_like.write("""\
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
 "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">

<svg width="%s" height="%s" version="1.1" xmlns="http://www.w3.org/2000/svg"
  xmlns:xlink="http://www.w3.org/1999/xlink">
<!-- automaticaly generated by aafigure and docutils -->
""" % (
                '100%', #self._num(self.width),
                '100%', #self._num(self.height)
            ))
        else:
            self.file_like.write("""<svg width="%s" height="%s" version="1.1" xmlns="http://www.w3.org/2000/svg">\n""" % (
                self._num(self.width),
                self._num(self.height)
            ))
        self.visit_shapes(aa_image.shapes)
        self.file_like.write("</svg>\n")
  
    def visit_shapes(self, shapes):
        for shape in shapes:
            shape_name = shape.__class__.__name__.lower()
            visitor_name = 'visit_%s' % shape_name
            if hasattr(self, visitor_name):
                getattr(self, visitor_name)(shape)
            else:
                print "WARNING: don't know how to handle shape %r" % shape

    # - - - - - - SVG drawing helpers - - - - - - -
    def _line(self, x1, y1, x2, y2, thick):
        """Draw a line, coordinates given as four decimal numbers"""
        self.file_like.write(
            """%s<line x1="%s" y1="%s" x2="%s" y2="%s" style="stroke:%s; stroke-width:%s;" />\n""" % (
            self.indent,
            self._num(x1),
            self._num(y1),
            self._num(x2),
            self._num(y2),
            self._color(self.foreground),
            self._unit(self.line_width*(1+bool(thick)))))

    def _rectangle(self, x1, y1, x2, y2, style=''):
        """Draw a rectange, coordinates given as four decimal numbers.
           ``style`` is inserted in the SVG. It could be e.g. "fill:yellow"
        """
        if x1 > x2: x1, x2 = x2, x1
        if y1 > y2: y1, y2 = y2, y1
        self.file_like.write("""\
%s<rect x="%s" y="%s" width="%s" height="%s" style="stroke:%s; fill:%s; stroke-width:%s; %s" />
""" % (
            self.indent,
            self._num(x1), self._num(y1),
            self._num(x2-x1), self._num(y2-y1),
            #~ self._color(self.foreground), #stroke:%s;
            self._color(self.fillcolor), #stroke:%s;
            self._color(self.fillcolor),
            self._unit(self.line_width),
            style
        ))

    # - - - - - - visitor function for the different shape types - - - - - - -
    
    def visit_point(self, point):
        self.file_like.write("""\
%s<circle cx="%s" cy="%s" r="%s" style="fill:%s; stroke:%s; stroke-width:%s;" />
""" % (
        self.indent,
        self._num(point.x), self._num(point.y),
        self._num(0.2),
        self._color(self.foreground), self._color(self.foreground),
        self._unit(self.line_width)))
    
    def visit_line(self, line):
        x1, x2 = line.start.x, line.end.x
        y1, y2 = line.start.y, line.end.y
        self._line(x1, y1, x2, y2, line.thick)
    
    def visit_rectangle(self, rectangle):
        self._rectangle(
            rectangle.p1.x, rectangle.p1.y,
            rectangle.p2.x, rectangle.p2.y
        )
        
    
    def visit_circle(self, circle):
        self.file_like.write("""\
%s<circle cx="%s" cy="%s" r="%s" style="stroke:%s; stroke-width:%s;" />
""" % (
        self.indent,
        self._num(circle.center.x), self._num(circle.center.y),
        self._num(circle.radius),
        self._color(self.foreground),
        self._unit(self.line_width)))

    def visit_label(self, label):
        #  font-weight="bold"   style="stroke:%s"
        self.file_like.write("""\
%s<text x="%s" y="%s" font-family="Arial,sans-serif" font-size="%s" style="fill:%s" >
  %s
%s</text>
""" % (
        self.indent,
        self._num(label.position.x), self._num(label.position.y-0.3), #XXX static offset not good in all situations
        self._num(self.aa_image.nominal_size),
        self._color(self.foreground),
        escape(label.text.encode('utf8')),
        self.indent
        ))

    def visit_group(self, group):
        self.file_like.write("<g>\n")
        old_indent = self.indent
        self.indent += '    '
        self.visit_shapes(group.shapes)
        self.indent = old_indent
        self.file_like.write("</g>\n")


