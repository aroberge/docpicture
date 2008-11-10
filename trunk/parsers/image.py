'''  Parser for the image directive, to embed images (local or located
on the web) as an html <img> object.
'''

import re
import src.svg as svg

def register_docpicture_parser(register_parser):
    register_parser(Image)

class Image(object):
    '''a parser creating web sequence diagrams'''
    def __init__(self):
        self.directive_name = 'image'
        self.params = {"src=": None,
                       }

    def create_picture(self, lines):
        '''Converts parsed lines of code
           into svg drawing statements'''
        self.extract_parameters(lines)
        return self.create_img_element()

    def extract_parameters(self, lines):
        '''extracts relevant parameters from instruction'''
        for line in lines:
            line = line.strip()
            if line == "":
                continue
            line = line.split("=")
            self.params[line[0].strip()] = line[1].strip()

    def create_img_element(self):
        '''creates an img xml element from the extracted parameters'''
        img = svg.XmlElement("img")
        for param in self.params:
            if self.params[param] is not None:
                img.attributes[param] = self.params[param]
        return img
