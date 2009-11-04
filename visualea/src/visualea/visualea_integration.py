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
"""This file customizes the grapheditor to work well with visualea"""


from PyQt4 import QtCore, QtGui
from graph_operator import GraphOperator
from openalea.core.pkgmanager import PackageManager
from openalea.core.node import RecursionError
from openalea.grapheditor import qtgraphview

#import visualea_integration_vertex

####################################################
# Handling the drag and drop events over the graph #
####################################################
def OpenAleaNodeFactoryHandler(view, event):
    """ Drag and Drop from the PackageManager """
    if (event.mimeData().hasFormat("openalea/nodefactory")):
        pieceData = event.mimeData().data("openalea/nodefactory")
        dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
        
        package_id = QtCore.QString()
        factory_id = QtCore.QString()
        
        dataStream >> package_id >> factory_id
        
        # Add new node
        pkgmanager = PackageManager()
        pkg = pkgmanager[str(package_id)]
        factory = pkg.get_factory(str(factory_id))
        
        position = view.mapToScene(event.pos())
        try:
            node = factory.instantiate([view.observed().factory.get_id()])
            view.graph.add_vertex(node, position=[position.x(), position.y()])
        except RecursionError:
            mess = QtGui.QMessageBox.warning(view, "Error",
                                             "A graph cannot be contained in itself.")
            return
        
        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()


def OpenAleaNodeDataPoolHandler(view, event):
    # Drag and Drop from the DataPool
    if(event.mimeData().hasFormat("openalea/data_instance")):
        pieceData = event.mimeData().data("openalea/data_instance")
        dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)

        data_key = QtCore.QString()

        dataStream >> data_key
        data_key = str(data_key)

        # Add new node
        pkgmanager = PackageManager()
        pkg = pkgmanager["system"]
        factory = pkg.get_factory("pool reader")

        position = view.mapToScene(event.pos())

        # Set key val
        try:
            node = factory.instantiate([view.observed().factory.get_id()])
            view.graph.add_vertex(node, [position.x(), position.y()])
        except RecursionError:
            mess = QtGui.QMessageBox.warning(view, "Error",
                                             "A graph cannot be contained in itself.")
            return

        node.set_input(0, data_key)
        node.set_caption("pool ['%s']"%(data_key,))

        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()


mimeFormats = ["openalea/nodefactory", "openalea/data_instance"]
mimeDropHandlers = [OpenAleaNodeFactoryHandler, OpenAleaNodeDataPoolHandler]
def get_drop_mime_handlers():
    return dict(zip(mimeFormats, mimeDropHandlers))

qtgraphview.QtGraphView.set_mime_handler_map(get_drop_mime_handlers())


#################################
# QtEvent handlers for vertices #
#################################

def vertexMouseDoubleClickEvent(graphItem, event):
    if event.button()==QtCore.Qt.LeftButton:
        # Read settings
        try:
            localsettings = Settings()
            str = localsettings.get("UI", "DoubleClick")
        except:
            str = "['open']"

        view = graphItem.scene().views()[0]
        operator=GraphOperator(view, graphItem.graph)
        operator.set_vertex_item(graphItem)

        if('open' in str):
            operator.vertex_open()
        elif('run' in str):
            operator.vertex_run()



def vertexContextMenuEvent(graphItem, event):
    """ Context menu event : Display the menu"""
    view = graphItem.scene().views()[0]
    operator=GraphOperator(view, graphItem.graph)
    operator.set_vertex_item(graphItem)
    menu = QtGui.QMenu(view)

    menu.addAction(operator("Run",             menu, "vertex_run"))
    menu.addAction(operator("Open Widget",     menu, "vertex_open"))
    menu.addSeparator()
    menu.addAction(operator("Delete",          menu, "vertex_remove"))
    menu.addAction(operator("Reset",           menu, "vertex_reset"))
    menu.addAction(operator("Replace By",      menu, "vertex_replace"))
    menu.addAction(operator("Reload",          menu, "vertex_reload"))
    menu.addSeparator()
    menu.addAction(operator("Caption",         menu, "vertex_set_caption"))
    menu.addAction(operator("Show/Hide ports", menu, "vertex_show_hide_ports"))
    menu.addSeparator()

    action = operator("Mark as User Application", menu, "vertex_mark_user_app")
    action.setCheckable(True)
    action.setChecked( bool(graphItem.vertex().user_application))
    menu.addAction(action)

    action = operator("Lazy", menu, "vertex_set_lazy")
    action.setCheckable(True)
    action.setChecked(graphItem.vertex().lazy)
    menu.addAction(action)

    action = operator("Block", menu, "vertex_block")
    action.setCheckable(True)
    action.setChecked(graphItem.vertex().block)
    menu.addAction(action)

    menu.addAction(operator("Internals", menu, "vertex_edit_internals"))

    menu.move(event.screenPos())
    menu.show()
    del menu
    event.accept()



qtgraphview.QtGraphViewVertex.set_event_handler("mouseDoubleClickEvent", 
                                                vertexMouseDoubleClickEvent)
qtgraphview.QtGraphViewVertex.set_event_handler("contextMenuEvent", 
                                                vertexContextMenuEvent)




##############################
# QtEvent handlers for edges #
##############################

#nothing special here the default 
#actions of the dataflow strategy
#are fine


####################################
# QtEvent handlers for annotations #
####################################

#nothing special here the default 
#actions of the dataflow strategy
#are fine
