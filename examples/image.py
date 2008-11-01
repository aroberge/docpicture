'''
Fake module to test image insertion.


We can embed any image located on the web, specifying any normal
attributes that is found in a given image. No error checking is performed.
A simple example is as follows:

..docpicture:: image
  src=http://imgs.xkcd.com/comics/python.png

A more complex example is the following. Note that spaces around the "=" sign
are unimportant.  Note also that the argument must *not* be surrounded by
quotes.

..docpicture:: image
  src    = http://imgs.xkcd.com/comics/python.png
  height = 20px
  width  = 30px
  style  = border: 10px solid red; background-color: blue; padding: 10px;




'''