import unittest
# Ensuring that the proper path is found; there must be a better way
import os
import sys
sys.path.insert(0, os.path.normpath(os.path.join(os.getcwd(), "..", "..")))
# other imports proceed

from parsers import turtle

class TestTurtle(unittest.TestCase):
    ''' description '''
    def setUp(self):
        self.t = turtle.Turtle()

    def test_extract_parameters(self):
        test_lines = ["turtle.color('red')", "turtle.up()", 
                    "turtle(23).forward(45)", 'turtle.color("green")', 
                    "turtle.down()", "turtle(67).right(9)", 
                    "turtle(89).left(21)"]
        test1 = test_lines[:3]
        result = []
        for line in test1:
            result.append(self.t.parse_single_line(line))
        self.t.extract_parameters(result)
        self.assert_(self.t.color == "red")
        self.assert_(self.t.command == "forward")
        self.assert_(self.t.arg == "45")
        self.assert_(self.t.angle1 == "23")
        self.assert_(not self.t.pen_down)
        self.assert_(self.t.mistakes is None)

        result = [self.t.parse_single_line(test_lines[4])]
        self.t.extract_parameters(result)
        self.assert_(self.t.color == "black")
        self.assert_(self.t.command is None)
        self.assert_(self.t.arg is None)
        self.assert_(self.t.angle1 is None)
        self.assert_(self.t.pen_down)
        self.assert_(self.t.mistakes)


        result = []
        for line in test_lines:
            result.append(self.t.parse_single_line(line))
        self.t.extract_parameters(result)
        self.assert_(self.t.color == "green")
        self.assert_(self.t.command == "left")
        self.assert_(self.t.arg == "21")
        self.assert_(self.t.angle1 == "89")
        self.assert_(self.t.pen_down)
        self.assert_(self.t.mistakes is None)

if __name__ == '__main__':
    unittest.main()