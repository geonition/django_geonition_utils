"""
This file includes generic widgets that are
commonly used in many applications
"""
from django.forms.widgets import Input
from django.forms.widgets import Widget

#basic html 5 widgets with fallback javascript

class NumberInput(Input):
    """
    Presents a html 5 input of type number
    
    remember to pass the render function args
    for name and value and additionaly if
    required attrs=<some attrs dict>
    """
    input_type = 'number'

class Paragraph(Widget):
    """
    This class represents a simple html
    paragraph.
    """
    def render(self, text):
        return u'<p>%s</p>' % text
    
class Radiobutton(Input):
    """
    This widget is a radiobutton
    """
    input_type = 'radio'
    
class Checkbox(Input):
    """
    This widget is a radiobutton
    """
    input_type = 'checkbox'
    
    
class ColorInput(Input):
    """
    This widget is a radiobutton
    """
    input_type = 'color'
    
class RangeInput(Input):
    """
    This widget is a radiobutton
    """
    input_type = 'range'
    
