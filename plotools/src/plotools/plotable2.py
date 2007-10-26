#!/usr/bin/env python
"""Definition of plotable object


Mainly based on mathplotlib.

:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    INRIA

szymon.stoma
82471946
"""
# Module documentation variables:
__authors__="""David Da Silva,
Szymon Stoma    
"""
__contact__=""
__license__="Cecill-C"
__date__="<Timestamp>"
__version__="0.1"
__docformat__= "restructuredtext en"
__revision__="$Id: plotable.py 805 2007-10-01 17:01:00Z stymek $"


import copy
import sys
from matplotlib import rc, rcParams,use
if("win" in sys.platform):
  print "LateX writing not available"
else:
  rc('text', usetex=True )
use('Qt4Agg')
import pylab

#the following allows a smooth use of pylab windows with Qt4.2#
try:
  from matplotlib.backends.backend_qt4 import qApp
except ImportError:
  import matplotlib as mymat
  from matplotlib.backends import backend_qt4, backend_qt4agg
  from PyQt4 import QtGui
  backend_qt4.qApp = QtGui.qApp
  backend_qt4agg.matplotlib = mymat
#=============================================================#


        
class VisualSequence(object):
    """Object containing basic plot information.
    
    <Long description of the function functionality.>    
    """

    def __init__( self, x=[], y=[], z=[], legend="", linestyle="", marker="", color="", bins=10, **keys ):
        """Object used to store plot information. 
        
        It use the syntax of mathplot lib so go there for details.
        
        :parameters:
            x : `[float]`
                X coordinates
            y : `[float]`
                values f(X)
            legend : `string`
                legend of a line
            linestyle : `string`
                One of - : -. -
            marker : `string`
                One of + , o . s v x > <,
            color : `string`
                A matplotlib color arg

        
        """
        # data segment -- should be shared between the views
        self.abs = x
        self.ord = y
        #self.x = x
        #self.y = y
        self.z = z
        
        # properties segment -- should be changed for each view
        
        self.legend = str(legend)
        self.linestyle = str(linestyle)
        self.marker = str(marker)
        self.color = str(color)
        self.bins = int(bins)

    def get_x(self):
        if len(self.abs) == len(self.ord):
            return self.abs
        else:
            return range(len(self.ord))
    def set_x(self, value):
        self.abs = value
    def get_y(self):
        return self.ord
    def set_y(self, value):
        self.ord = value

    x = property(get_x, set_x)
    y = property(get_y, set_y)


def change_VisualSequence_PointLineView( vis_seq, new_legend, new_linestyle, new_marker, new_color ): 
        """Returns vis_seq object with values changed from default
        
        :parameters:
            vis_seq : `VisualSequence`
                object to be modified
            legend : `string`
                legend of a line
            linestyle : `string`
                One of - : -. -
            marker : `string`
                One of + , o . s v x > <,
            color : `string`
                A matplotlib color arg
        :rtype: `VisualSequence`
        :return: Updated object.
        """
        plotable = copy.copy(vis_seq)
        if not new_linestyle=="Default":
            plotable.linestyle = str( new_linestyle )
        if not new_marker=="Default":
            plotable.marker = str( new_marker )
        if not new_color=="Default":
            plotable.color = str( new_color )
        if not new_legend=="Default":
            plotable.legend =  str( new_legend )
        return  plotable

def display_VisualSequence(  vis_seq_list=list(), visualisation="", title="", xlabel="", ylabel="", figure=0, **keys ):
    """Plots 2D visual sequences.
    
    :parameters:
        vis_seq_list : `[VisualSequence]`
            Contains a list of object to display
        title : `string`
            Title of the plot.
        xlabel : `string`
            X axis description
        ylabel : `string`
            Y label description
    """
    if visualisation == 'Hist':
        return display_VisualSequence_as_Hist( vis_seq=vis_seq_list, title=title, xlabel=xlabel, ylabel=ylabel, figure=figure, **keys )
    elif visualisation == 'PointLine':
        return display_VisualSequence_as_PointLine( vis_seq_list=vis_seq_list, title=title, xlabel=xlabel, ylabel=ylabel, figure=figure, **keys )
    raise TypeError("Any know plot type")

def display_VisualSequence_as_PointLine(  vis_seq_list=list(), title="", xlabel="", ylabel="", figure=0, **keys ):
    """Plots 2D visual sequences.
    
    :parameters:
        vis_seq_list : `[VisualSequence]`
            Contains a list of object to display
        title : `string`
            Title of the plot.
        xlabel : `string`
            X axis description
        ylabel : `string`
            Y label description
    """
    objList=vis_seq_list
    pylab.figure( figure )
    pylab.cla()
    legend_printed = False
    try:
        iter( objList )
        legend =[]
        for obj in objList :
            pylab.plot( obj.x, obj.y, linestyle=obj.linestyle, marker=obj.marker, color=obj.color, markerfacecolor=obj.color, **keys )
            if obj.legend:
                legend.append(r''+obj.legend )
                legend_printed = True
        if legend_printed: pylab.legend( tuple( legend ), loc='best', shadow=True )
    except  TypeError:
        # do sth with exceptions
        obj=vis_seq_list
        #print figure
        pylab.plot( obj.x, obj.y, linestyle=obj.linestyle, marker=obj.marker, color=obj.color, markerfacecolor=obj.color,  **keys )

    xmin, xmax = pylab.xlim()
    xr = (xmax-xmin)/20.
    pylab.xlim(xmin-xr, xmax+xr)
    ymin, ymax = pylab.ylim()
    yr = (ymax-ymin)/20.
    pylab.ylim(ymin-yr, ymax+yr)
    pylab.title( title )
    pylab.xlabel( xlabel )
    pylab.ylabel( ylabel )
    pylab.show()


def change_VisualSequence_HistView( vis_seq,  new_bins, new_color ): 
        """Returns vis_seq object with values changed from default
        
        :parameters:
            vis_seq : `VisualSequence`
                object to be modified
            legend : `string`
                legend of a line
            linestyle : `string`
                One of - : -. -
            marker : `string`
                One of + , o . s v x > <,
            color : `string`
                A matplotlib color arg
        :rtype: `VisualSequence`
        :return: Updated object.
        """
        plotable = copy.copy(vis_seq)
        if not new_color=="Default":
            plotable.color = str( new_color )
        if not new_bins==10:
            plotable.new_bins =  int( new_bins )
        return  plotable


def display_VisualSequence_as_Hist(  vis_seq=[], title="", xlabel="", ylabel="", figure=0, **keys ):
    """Plots 2D visual sequences.
    
    :parameters:
        vis_seq_list : `[VisualSequence]`
            Contains a list of object to display
        title : `string`
            Title of the plot.
        xlabel : `string`
            X axis description
        ylabel : `string`
            Y label description
    """
    pylab.figure( figure )
    pylab.cla()
    pylab.hist(vis_seq.y, vis_seq.bins, **keys )
    pylab.title( title )
    pylab.xlabel( xlabel )
    pylab.ylabel( ylabel )
    pylab.show()


def seqs2VisualSequence( seq1=[], seq2=[], marker="o", color="b", **keys ):
    """generates visual sequence2D with list1 as x  and list2 as y
    
    :parameters:
        seq1 : `iterable`
            Contains the x sequence
        seq2 : `iterable`
            Contains the x sequence
        marker : `string`
            The marker for the Point-Line.
        color : `string`
            The color.
    """
    return VisualSequence(x=seq1, y=seq2,z=None, marker=marker, color=color, **keys )
       

def dict2VisualSequence(  dict2vis_seq={}, marker="o", color="g", **keys ):
    """generates visual sequence2D with keys as x  and values as y
    
    :parameters:
        dict2vis_seq : `dict{float:float}`
            Contains a list of object to display
        marker : `string`
            The marker for the Point-Line.
        color : `string`
            The color.
    """
    r=list(dict2vis_seq.items())
    r.sort()
    return VisualSequence(x=[r[i][0] for i in range(len(r))], y=[r[i][1] for i in range(len(r))],z=None, marker=marker, color=color, **keys )

