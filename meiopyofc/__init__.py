import elements
import series
from util import OfcDict
from django.utils import simplejson
from values import Value

def flashHTML(width, height, url, ofc_base_url="/flashes/", ofc_swf="OFC.swf" ):
    '''
    From open-flash-chart-python project. Create the HTML needed to display the chart.
    URL: http://code.google.com/p/open-flash-chart-python/
    '''
    return (
        """
        <object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000"
                codebase="http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,115,0"
                width="%(width)s" height="%(height)s" id="chart" align="middle">
            <param name="allowScriptAccess" value="sameDomain"/>
            <param name="movie" value="%(ofc_base_url)s%(ofc_swf)s"/>
            <param name="FlashVars" value="data-file=%(url)s"/>
            <param name="quality" value="high"/>
            <param name="bgcolor" value="#FFFFFF"/>
            <embed src="%(ofc_base_url)s%(ofc_swf)s" FlashVars="data-file=%(url)s" quality="high" bgcolor="#FFFFFF"
                   width=%(width)s height=%(height)s name="chart" align="middle" allowScriptAccess="sameDomain"
                   type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer"/>
        </object>
        """) % locals()

class Chart(OfcDict):
    types = {
        'title': elements.Title,
        'x_legend': elements.XLegend,
        'y_legend': elements.YLegend,
        'x_axis': elements.XAxis,
        'y_axis': elements.YAxis,
        'y_axis_right': elements.YAxis,
        # TODO! Add radar axis
        'bg_colour': elements.Colour,
        'tooltip': elements.Tooltip,
        'elements': series.SeriesList,
    }
    
    def __init__(self, dictionary={}, auto_ranges=True):
        self.auto_ranges = True
        super(Chart, self).__init__(dictionary)
    
    def calculate_range_y(self):
        '''
        Gets the max and min values of the chart elements and applies these values to
        the y axis max and min attributes.
        '''
        min_value, max_value = (2147483647.0,-2147483647)
        for element in self['elements']:
            for value in element['values']:
                if isinstance(value, Value):
                    max_value = max(value.get('value',max_value),value.get('top',max_value),max_value)
                    min_value = min(value.get('value',min_value),value.get('bottom',min_value),min_value)
                else:
                    max_value = max(value, max_value)
                    min_value = min(value, min_value)
        min_value -= 1
        max_value += 1
        if min_value > 0:
            min_value = 0
        self['y_axis']['min'] = min_value
        self['y_axis']['max'] = max_value
        steps = int((max_value-min_value)/5)
        if steps > 1:
            self['y_axis']['steps'] = steps
    
    def encode(self):
        '''
        Returns this Chart object JSON format
        '''
        if self.auto_ranges:
            self.calculate_range_y()
        self.clean_nulls()
        return simplejson.dumps(self)
