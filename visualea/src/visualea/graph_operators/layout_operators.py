# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from PyQt4 import QtGui, QtCore
from openalea.grapheditor import qtgraphview

class LayoutOperators(object):
    def graph_align_selection_horizontal(self):
        """Align all items on a median ligne.
        """
        widget = self.graphView()
        
        if widget is None :
            return
        
        items = widget.get_selected_items(qtgraphview.QtGraphViewVertex)
        if len(items) > 1 :
            #find median base #TODO beware of relative to parent coordinates
            ymean = sum(item.pos().y() for item in items) / len(items)
            
            #move all items
            for item in items :
                item.setPos(item.pos().x(),ymean)
        
            #notify
            widget.notify(None,("graph_modified",) )
        
        return

    def graph_align_selection_left (self):
        """Align all items on their left side.
        """
        widget = self.graphView()        
        if widget is None :
            return
        
        items = widget.get_selected_items(qtgraphview.QtGraphViewVertex)
        if len(items) > 1 :
            #find left ligne #TODO beware of relative to parent coordinates
            xmean = sum(item.pos().x() for item in items) / len(items)
            
            #move all items
            for item in items :
                item.setPos(xmean,item.pos().y() )
        
            #notify
            widget.notify(None,("graph_modified",) )
        
        return

    def graph_align_selection_right (self):
        """Align all items on their right side.
        """
        widget = self.graphView()
        if widget is None :
            return
        
        items = widget.get_selected_items(qtgraphview.QtGraphViewVertex)
        if len(items) > 1 :
            #find left ligne #TODO beware of relative to parent coordinates
            xmean = sum(item.pos().x() + \
                        item.boundingRect().width() \
                        for item in items) / len(items)
            
            #move all items
            for item in items :
                item.setPos(xmean - item.boundingRect().width(),item.pos().y() )
        
            #notify
            widget.notify(None,("graph_modified",) )
        
        return

    def graph_align_selection_mean (self):
        """Align all items vertically around a mean ligne.
        """
        widget = self.graphView()        
        if widget is None :
            return

        items = widget.get_selected_items(qtgraphview.QtGraphViewVertex)        
        if len(items) > 1 :
            #find left ligne #TODO beware of relative to parent coordinates
            xmean = sum(item.pos().x() + \
                        item.boundingRect().width() / 2. \
                        for item in items) / len(items)
            
            #move all items
            for item in items :
                item.setPos(xmean - item.boundingRect().width() / 2.,item.pos().y() )
        
            #notify
            widget.notify(None,("graph_modified",) )
        
        return

    def graph_distribute_selection_horizontally (self):
        """distribute the horizontal distances between items.
        """
        widget = self.graphView()        
        if widget is None :
            return
        
        items = widget.get_selected_items(qtgraphview.QtGraphViewVertex)        
        if len(items) > 2 :
            #find xmin,xmax of selected items #TODO beware of relative to parent coordinates
            xmin = min(item.pos().x() for item in items)
            xmax = max(item.pos().x() + item.boundingRect().width() \
                       for item in items)
            
            #find mean distance between items
            dist = ( (xmax - xmin) - \
                   sum(item.boundingRect().width() for item in items) )\
                   / (len(items) - 1)
            
            #sort all items by their mean position
            item_centers = [(item.pos().x() + item.boundingRect().width() / 2.,item) for item in items]
            item_centers.sort()
            
            #move all items
            first_item = item_centers[0][1]
            current_x = first_item.pos().x() + first_item.boundingRect().width()
            
            for x,item in item_centers[1:-1] :
                item.setPos(current_x + dist,item.pos().y() )
                current_x += dist + item.boundingRect().width()
        
            #notify
            widget.notify(None,("graph_modified",) )
        
        return

    def graph_distribute_selection_vertically (self):
        """distribute the vertical distances between items.
        """
        widget = self.graphView()
        if widget is None :
            return
        
        items = widget.get_selected_items(qtgraphview.QtGraphViewVertex)        
        if len(items) > 1 :
            #find ymin,ymax of selected items #TODO beware of relative to parent coordinates
            ymin = min(item.pos().y() for item in items)
            ymax = max(item.pos().y() + item.boundingRect().height() \
                       for item in items)
            
            #find mean distance between items
            dist = ( (ymax - ymin) - \
                   sum(item.boundingRect().height() for item in items) )\
                   / (len(items) - 1)
            
            #sort all items by their mean position
            item_centers = [(item.pos().y() + item.boundingRect().height() / 2.,item) for item in items]
            item_centers.sort()
            
            #move all items
            first_item = item_centers[0][1]
            current_y = first_item.pos().y() + first_item.boundingRect().height()
            
            for y,item in item_centers[1:-1] :
                item.setPos(item.pos().x(),current_y + dist)
                current_y += dist + item.boundingRect().height()
            
            #notify
            widget.notify(None,("graph_modified",) )
        
        return
