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
__revision__ = " $Id: vertex.py 2016 2009-12-16 12:55:01Z dbarbeau $ "

from PyQt4 import QtGui, QtCore
import weakref, gc #gc is needed because there is a collection problem with the node inspector
from openalea.visualea.util import open_dialog
from openalea.visualea.dialogs import DictEditor, ShowPortDialog, NodeChooser
from openalea.grapheditor import qtgraphview #no need to reload the dataflow package.

class VertexOperators(object):
    def __init__(self):
        # ---reference to the widget of this vertex---
        self._vertexWidget = None
        self.vertexItem = None

    def set_vertex_item(self, vertexItem):
        self.vertexItem = weakref.ref(vertexItem)

    def vertex_composite_inspect(self):
        #collect dangling PyQt objects which have lost their C++ side.
        #There is probably a circular reference somewhere in the dataflowview code
        #that prevents dead GraphicalVertex instances to be collected by simple
        #reference counting. I haven't found it so for the moment, we use this
        #workaround:
        widget = qtgraphview.View(self.get_graph_view(), self.vertexItem().vertex())
        widget.setWindowFlags(QtCore.Qt.Window)
        widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        widget.connect(widget, QtCore.SIGNAL("destroyed(QObject*)"), gc.collect)
        widget.show()
        
    def vertex_run(self):
        self.get_graph().eval_as_expression(self.vertexItem().vertex().get_id())        

    def vertex_open(self):
        if(self._vertexWidget):
            if(self._vertexWidget.isVisible()):
                self._vertexWidget.raise_ ()
                self._vertexWidget.activateWindow ()
            else:
                self._vertexWidget.show()
            return

        factory = self.vertexItem().vertex().get_factory()
        if(not factory) : return
        # Create the dialog. 
        # NOTE: WE REQUEST THE MODEL TO CREATE THE DIALOG
        # THIS IS NOT DESIRED BECAUSE IT COUPLES THE MODEL
        # TO THE UI.
        innerWidget = factory.instantiate_widget(self.vertexItem().vertex(), None)
        if(not innerWidget) : return 
        if (innerWidget.is_empty()):
            innerWidget.close()
            del innerWidget
            return

        self._vertexWidget = open_dialog(self.get_graph_view(), innerWidget, factory.get_id(), False)

    def vertex_remove(self):
        self.get_graph().remove_vertex(self.vertexItem().vertex())

    def vertex_reset(self):
        self.vertexItem().vertex().reset()

    def vertex_replace(self):
        """ Replace a node by an other """
        
        self.dialog = NodeChooser(self.get_graph_view())
        self.dialog.search('', self.vertexItem().vertex().get_nb_input(), 
                           self.vertexItem().vertex().get_nb_output())
        ret = self.dialog.exec_()

        if(not ret): return
        
        factory = self.dialog.get_selection()
        newnode = factory.instantiate()
        self.get_graph().replace_vertex(self.vertexItem().vertex(), newnode)

    def vertex_reload(self):
        """ Reload the vertex """

        # Reload package
        factory = self.vertexItem().vertex().factory
        package = factory.package
        if(package):
            package.reload()

        # Reinstantiate the vertex
        newvertex = factory.instantiate()
        self.get_graph().set_actor(self.vertexItem().vertex().get_id(), newvertex)
        newvertex.internal_data.update(self.vertexItem().vertex().internal_data)
        self.vertexItem().set_observed(newvertex)
        self.vertexItem().initialise_from_model()

    def vertex_set_caption(self):
        """ Open a input dialog to set node caption """

        n = self.vertexItem().vertex()
        (result, ok) = QtGui.QInputDialog.getText(None, "Node caption", "",
                                   QtGui.QLineEdit.Normal, n.caption)
        if(ok):
            n.caption = str(result) #I HATE PROPERTIES, REALLY!

    def vertex_show_hide_ports(self):
        """ Open port show/hide dialog """
        editor = ShowPortDialog(self.vertexItem().vertex(), self.get_graph_view())
        editor.exec_()

    def vertex_mark_user_app(self, val):
        self.get_graph().set_continuous_eval(self.vertexItem().vertex().get_id(), bool(val))

    def vertex_set_lazy(self, val):
        self.vertexItem().vertex().lazy = val #I DO HATE PROPERTIES, REALLY!

    def vertex_block(self, val):
        self.vertexItem().vertex().block = val #I DEFINITELY DO HATE PROPERTIES, REALLY!

    def vertex_edit_internals(self):
        """ Edit node internal data """
        editor = DictEditor(self.vertexItem().vertex().internal_data, self.get_graph_view())
        ret = editor.exec_()

        if(ret):
            for k in editor.modified_key:
                self.vertexItem().vertex().set_data(k, editor.pdict[k])
