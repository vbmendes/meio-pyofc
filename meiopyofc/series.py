from util import OfcDict
from elements import Colour, ColoursList, LineStyle
from values import ValuesList, ShapePointsList, Value, BarValue
import conf

class SeriesList(list):
    colours = conf.colours
    value_colours = {
        'positive': '#009900',
        'negative': '#990000',
        'zero': '#000099',
    }
    def append(self, series):
        if series.colorize_series:
            series['colour'] = self.colours[len(self)%len(self.colours)]
        super(SeriesList, self).append(series)

class Series(OfcDict):
    types = {
        'type': str,
        'alpha': float,
        'colour': Colour,
        'gradient-fill': str,
        'halo-size': int,
        'width': int,
        'dot-size': int,
        'text': str,
        'font-size': int,
        'values': ValuesList,
        'line-style': LineStyle,
        'tip': str,
        'no-labels': bool,
        'loop': bool,
        'on-click': str,
    }
    value_cls = Value
    
    def __init__(self, dictionary, colorize_series=True):
        self.colorize_series = colorize_series
        super(Series, self).__init__(dictionary)
                
class OutlineSeries(Series):
    types = {
        'outline-colour': Colour
    }

# TODO! Keys in bar stacks

class Line(Series):
    colors = {
        'p': '#009900',
        'z': '#000099',
        'n': '#990000',
    }

    COLORIZE_NONE, COLORIZE_NEGATIVES, \
    COLORIZE_ZEROS, COLORIZE_ZEROS_NEGATIVES, \
    COLORIZE_POSITIVES, COLORIZE_POSITIVES_NEGATIVES, \
    COLORIZE_PORITIVES_ZEROS, COLORIZE_ALL = range(8)

    def __init__(self, dictionary, colorize_values=COLORIZE_ALL, **kwargs):
        self.colorize_values = colorize_values
        dictionary['type'] = dictionary.get('type', 'line')
        super(Line, self).__init__(dictionary, **kwargs)
        
    def _process_values(self, values):
        #return values
        return self.colorized_values(values)
    
    def colorized_values(self, values, colors=None):
        if not colors:
            colors = self.colors
        
        colorize_positives = bool(self.colorize_values/4) and 'p' in colors
        colorize_zeros = bool((self.colorize_values%4)/2) and 'z' in colors
        colorize_negatives = bool(self.colorize_values%2) and 'n' in colors
        
        for k in range(len(values)):
            value = values[k]
            if isinstance(value, Value):
                num_value = float(value['value'])
            else:
                num_value = float(value)
            
            if num_value < 0:
                if colorize_negatives:
                    values[k] = self.colorize_value(value, colors['n'])
            elif num_value > 0:
                if colorize_positives:
                    values[k] = self.colorize_value(value, colors['p'])
            else:
                values[k] = self.colorize_value(value, colors['z'])
        return values
    
    def colorize_value(self, value, color):
        if isinstance(value, self.value_cls):
            value['colour'] = color
            return value
        else:
            return self.value_cls({'value': value, 'colour': color})

class LineDot(Line):
    def __init__(self, dictionary, **kwargs):
        dictionary['type'] = 'line_dot'
        super(LineDot, self).__init__(dictionary, **kwargs)
        
class LineHollow(Line):
    def __init__(self, dictionary, **kwargs):
        dictionary['type'] = 'line_hollow'
        super(LineHollow, self).__init__(dictionary, **kwargs)

class Bar(Series):
    def __init__(self, dictionary, **kwargs):
        dictionary['type'] = 'bar'
        super(Bar, self).__init__(dictionary, **kwargs)

class BarFilled(OutlineSeries):
    def __init__(self, dictionary, **kwargs):
        dictionary['type'] = 'bar_filled'
        super(BarFilled, self).__init__(dictionary, **kwargs)

class BarGlass(Series):
    def __init__(self, dictionary, **kwargs):
        dictionary['type'] = 'bar_glass'
        kwargs['colorize_series'] = kwargs.get('colorize_series', False)
        super(BarGlass, self).__init__(dictionary, **kwargs)

class Bar3d(Series):
    def __init__(self, dictionary, **kwargs):
        dictionary['type'] = 'bar_3d'
        super(Bar3d, self).__init__(dictionary, **kwargs)

class BarSketch(OutlineSeries):
    def __init__(self, dictionary, **kwargs):
        dictionary['type'] = 'bar_sketch'
        super(BarSketch, self).__init__(dictionary, **kwargs)

class HBar(Series):
    def __init__(self, dictionary, **kwargs):
        dictionary['type'] = 'hbar'
        super(HBar, self).__init__(dictionary, **kwargs)

class BarStack(Series):
    types = {
        'colours': ColoursList,
    }
    def __init__(self, dictionary, **kwargs):
        dictionary['type'] = 'bar_stack'
        super(BarStack, self).__init__(dictionary, **kwargs)

class AreaLine(Series):
    types = {
        'fill-alpha': float,
        'fill': Colour,
    }
    def __init__(self, dictionary, **kwargs):
        dictionary['type'] = 'area_line'
        super(AreaLine, self).__init__(dictionary, **kwargs)

class AreaHollow(AreaLine):
    def __init__(self, dictionary, **kwargs):
        dictionary['type'] = 'area_hollow'
        super(AreaHollow, self).__init__(dictionary, **kwargs)

class Pie(Series):
    types = {
        'start-angle': int,
        'animate': bool,
        'colours': ColoursList,
        'label-colour': Colour,
    }
    def __init__(self, dictionary, **kwargs):
        dictionary['type'] = 'pie'
        dictionary['colours'] = conf.colours
        super(Pie, self).__init__(dictionary, **kwargs)

class Scatter(Series):
    def __init__(self, dictionary, **kwargs):
        dictionary['type'] = 'scatter'
        super(Scatter, self).__init__(dictionary, **kwargs)

class ScatterLine(Series):
    def __init__(self, dictionary, **kwargs):
        dictionary['type'] = 'scatter_line'
        super(ScatterLine, self).__init__(dictionary, **kwargs)

class Shape(OfcDict):
    types = {
        'type': str,
        'colour': Colour,
        'values': ShapePointsList
    }
    
    def __init__(self, dictionary, **kwargs):
        dictionary['type'] = 'shape'
        super(Shape, self).__init__(dictionary, **kwargs)
