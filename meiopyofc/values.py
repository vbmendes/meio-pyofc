from util import OfcDict
from elements import Colour

class ValuesList(list):
    pass

class Value(OfcDict):
    types = {
        'value': float,
        'colour': Colour,
        'tip': str,
    }

class BarValue(Value):
    types = {
        'top': float,
        'bottom': float,
    }

class HbarValue(Value):
    types = {
        'left': float,
        'right': float,
    }

class PieValue(Value):
    types = {
        'label': str,
        'label-colour': Colour,
        'font-size': int,
    }

class ScatterValue(Value):
    types = {
        'x': float,
        'y': float,
    }

class BarStackKey(OfcDict):
    types = {
        'colour': Colour,
        'text': str,
        'font-size': int,
    }

class ShapePoint(OfcDict):
    types = {
        'x': float,
        'y': float,
    }

class ShapePointsList(list):
    pass
