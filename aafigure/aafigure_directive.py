"""
implement aafigure directive
"""

import os, sys, tempfile, popen2
#~ import cStringIO
import aafigure
import svg
try:
    import pil
except ImportError:
    #no support for bitmaps
    pil = None

from docutils import nodes
from docutils.parsers.rst.directives import register_directive, flag

DEFAULT_FORMAT = 'svg'
#~ DEFAULT_FORMAT = 'png'

aafigure_counter = 0

def decode_color(color_string):
    if color_string[0] == '#':          #HTML like color syntax
        if len(color_string) == 4:      # #rgb format
            r,g,b = [int(c+c, 16) for c in color_string[1:]]
        elif len(color_string) == 7:      # #rrggbb format
            r,g,b = [int(color_string[n:n+2], 16) for n in range(1, len(color_string), 2)]
        else:
            raise ValueError('not a valid color: %r' % color_string)
    #XXX add a list of named colors
    return r,g,b


def AAFigureDirective(name, arguments, options, content, lineno,
                  content_offset, block_text, state, state_machine):
    text = '\n'.join(content)
    
    global aafigure_counter
    
    #ensure that options are present and initialized with defaults if not given
    if not options.has_key('background'): options['background'] = '#ffffff'
    if not options.has_key('foreground'): options['foreground'] = '#000000'
    if not options.has_key('fill'): options['fill'] = options['foreground'] #fill = fore by default
    if not options.has_key('scale'): options['scale'] = 1
    if not options.has_key('line_width'): options['line_width'] = 2
    if not options.has_key('format'): options['format'] = DEFAULT_FORMAT
    if not options.has_key('aspect'): options['aspect'] = 1
    if not options.has_key('name'):
        options['name'] = 'aafigure-%i' % aafigure_counter
        aafigure_counter += 1
    
    aaimg = aafigure.AsciiArtImage(
        text,
        aspect_ratio = options['aspect'],
        textual = options.has_key('textual')
    )
    aaimg.recognize()
    
    if options['format'] == 'svg':
        output_name = options['name'] + '.svg'
        #~ io = cStringIO.StringIO()
        svgout = svg.SVGOutputVisitor(
            file(output_name, 'w'),
            #~ io,
            scale = options['scale']*6,
            line_width = options['line_width'],
            foreground = decode_color(options['foreground']),
            background = decode_color(options['background']),
            fillcolor = decode_color(options['fill'])
        )
        svgout.visit_image(aaimg)
        #~ svgout.visit(aaimg, xml_header = False)
        #insert data into html using a raw node
        attributes = {'format': 'html'}
        #~ # result = [nodes.raw('', '<embed src="%s" %s type="image/svg+xml"/>' % (
        result = [nodes.raw('', '<object type="image/svg+xml" data="%s" %s></object>' % (
            output_name,
            svgout.get_size_attrs()
        ), **attributes)]
        #~ result = [nodes.raw('', io.getvalue(), **attributes)]
    elif options['format'] == 'pdf':
        import pdf
        output_name = options['name'] + '.pdf'
        doc = pdf.PDFOutputVisitor(
            file(output_name, 'wb'),
            scale = options['scale'],
            line_width = options['line_width'],
            foreground = decode_color(options['foreground']),
            background = decode_color(options['background']),
            fillcolor = decode_color(options['fill']),
        )
        doc.visit_image(aaimg)
        # Return a link.
        wrapper = nodes.generated()
        wrapper.append(nodes.reference('', '%s (PDF)' % options['name'], 
            refuri=os.path.basename(output_name)
        ))
        result = [wrapper]
    elif pil is not None:
        output_name = '%s.%s' % (options['name'], options['format'])
        pilout = pil.PILOutputVisitor(
            file(output_name, 'wb'),
            scale = options['scale']*7,
            line_width = options['line_width'],
            debug = True,
            file_type = options['format'],
            foreground = decode_color(options['foreground']),
            background = decode_color(options['background']),
            fillcolor = decode_color(options['fill']),
        )
        try:
            pilout.visit_image(aaimg)
        except KeyError:
            result = [state_machine.reporter.error(
                'No support for image format %r' % (options['format']),
                nodes.literal_block(block_text, block_text),
                line=lineno
            )]
        else:
            # Return an image directive.
            image_options = {}
            image_options['uri'] = os.path.basename(output_name)
            result = [nodes.image(output_name, **image_options)]
    else:
        result = [state_machine.reporter.error(
            'No support for image format %r (PIL not installed)' % (options['format']),
            nodes.literal_block(block_text, block_text),
            line=lineno
        )]
    
    return result

AAFigureDirective.content = True
#~ AAFigureDirective.arguments = (1, 1, 1)
AAFigureDirective.options = {
    'scale': float,
    'line_width': float,
    'format': str,
    'name': str,
    'background': str,
    'foreground': str,
    'fill': str,
    'aspect': float,
    'textual': flag,
}

def register():
    register_directive('aafigure', AAFigureDirective)
