from util import OfcDict

class Colour(str):
    pass

class ColoursList(list):
    pass

class LineStyle(OfcDict):
    types = {
        'style': str,
        'on': int,
        'off': int,
    }
    
    def __init__(self, dictionary):
        if 'style' not in dictionary:
            dictionary['style'] = 'dash'
        if 'on' not in dictionary:
            dictionary['on'] = 1
        if 'off' not in dictionary:
            dictionary['off'] = 1
        super(LineStyle, self).__init__(dictionary)

class Label(OfcDict):
    types = {
        'colour': Colour,
        'text': str,
        'size': int,
        'rotate': str,
    }
    
class XLabel(Label):
    types = {
        'visible': bool,
        'align': str,
        'x': int
    }
    
class YLabel(Label):
    types = {
        'y': int,
    }
    
class LabelList(list):
    pass

class Labels(Label):
    types = {
        'steps': int,
        'labels': LabelList
    }
    
class XLabels(Labels):
    types = {
        'align': str,
        'visible': bool,
        'visible-steps': int,
    }
    
class YLabels(Labels):
    types = {
        'show_labels': bool,
    }
    
class Title(OfcDict):
    types = {
        'text':  str,
        'style':  str,
    }
    
    def clean_nulls(self):
        if not self['text']:
            del self['text']
            del self['style']

class YLegend(Title):
    pass

class XLegend(Title):
    pass

class Axis(OfcDict):
    types = {
        'stroke': int,
        'colour': Colour,
        'grid-colour': Colour,
        'steps': int,
        'offset': bool,
        'max': int,
        'min': int,
        '3d': int,
    }
    
class XAxis(Axis):
    types = {
        'tick-height': int,
        'labels': XLabels,
    }
    
class YAxis(Axis):
    types = {
        'tick-length': int,
        'labels': YLabels,
    }
    
#TODO! Radar Axis

class Tooltip(OfcDict):
    types = {
        'shadow': bool,
        'stroke': int,
        'colour': Colour,
        'background': Colour,
        'title': str,
        'body': str,
        'mouse': int
    }
    
    def _process_mouse(self, value):
        '''
        Function called before mouse assignment. It checks if the value is 1 or
        2, if so, returns the current value, otherwise it checks if the value is
        proximity or hover, returning the respective value for each of these
        words.
        '''
        if value in range(1,3):
            return value
        elif value == 'proximity':
            return 1
        elif value == 'hover':
            return 2
        else:
            return None


