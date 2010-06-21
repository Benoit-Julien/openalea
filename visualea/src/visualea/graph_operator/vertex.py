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
import weakref
from openalea.visualea.util import busy_cursor, exception_display, open_dialog
from openalea.visualea.dialogs import DictEditor, ShowPortDialog, NodeChooser

from openalea.core import observer, node
import compositenode_inspector

#To handle availability of actions automatically
from openalea.grapheditor import interactionstates as OAGIS
interactionMask = OAGIS.make_interaction_level_decorator()

class VertexOperators(object):
    __vertexWidgetMap__ = weakref.WeakKeyDictionary()

    def __init__(self):
        # ---reference to the widget of this vertex---
        self._vertexWidget = None
        self.vertexItem = None

    def set_vertex_item(self, vertexItem):
        self.vertexItem = weakref.ref(vertexItem)

    @interactionMask(OAGIS.EDITIONLEVELLOCK_1)
    def vertex_composite_inspect(self):
        widget = compositenode_inspector.Inspector(self.get_graph_view(),
                                                   self.vertexItem().vertex(),
                                                   self.get_main().operator,
                                                   self)
        widget.show_entire_scene()
        widget.show()

    @exception_display
    @busy_cursor
    @interactionMask(OAGIS.EDITIONLEVELLOCK_1)
    def vertex_run(self):
        self.get_graph().eval_as_expression(self.vertexItem().vertex().get_id())


    @interactionMask(OAGIS.EDITIONLEVELLOCK_1)
    def vertex_open(self):
        vertex = self.vertexItem().vertex()

        vwidget = VertexOperators.__vertexWidgetMap__.get(vertex, None)
        if(vwidget):
            if(vwidget.isVisible()):
                vwidget.raise_ ()
                vwidget.activateWindow ()
            else:
                vwidget.show()
            return

        # Create the dialog.
        # NOTE: WE REQUEST THE MODEL TO CREATE THE DIALOG
        # THIS IS NOT DESIRED BECAUSE IT COUPLES THE MODEL
        # TO THE UI.
        factory = vertex.get_factory()
        if(not factory) : return
        innerWidget = factory.instantiate_widget(vertex, None)
        if(not innerWidget) : return
        if (innerWidget.is_empty()):
            innerWidget.close()
            del innerWidget
            return

        VertexOperators.__vertexWidgetMap__[vertex] = open_dialog(self.get_graph_view(),
                                                                  innerWidget,
                                                                  factory.get_id(),
                                                                  False)

    @interactionMask(OAGIS.TOPOLOGICALLOCK)
    def vertex_remove(self):
        self.get_graph().remove_vertex(self.vertexItem().vertex())

    @interactionMask(OAGIS.EDITIONLEVELLOCK_1)
    def vertex_reset(self):
        self.vertexItem().vertex().reset()

    @interactionMask(OAGIS.TOPOLOGICALLOCK)
    def vertex_observer_copy(self, oldVertex, newVertex):
        """ Copies attributes from old vertex to new vertex, including listeners."""
        oldVertex.copy_to(newVertex)

    @exception_display
    @busy_cursor
    @interactionMask(OAGIS.TOPOLOGICALLOCK)
    def vertex_replace(self):
        """ Replace a node by an other """
        self.dialog = NodeChooser(self.get_graph_view())
        self.dialog.search('', self.vertexItem().vertex().get_nb_input(),
                           self.vertexItem().vertex().get_nb_output())
        ret = self.dialog.exec_()
        if(not ret): return

        factory = self.dialog.get_selection()
        oldVertex = self.vertexItem().vertex()
        newVertex = factory.instantiate()
        self.get_graph().replace_vertex(oldVertex, newVertex)
        self.vertex_observer_copy(oldVertex, newVertex)

    @interactionMask(OAGIS.EDITIONLEVELLOCK_1)
    def vertex_reload(self):
        """ Reload the vertex """
        # Reload package
        factory = self.vertexItem().vertex().factory
        package = factory.package
        if(package):
            package.reload()

        # Reinstantiate the vertex
        newVertex = factory.instantiate()
        oldVertex = self.vertexItem().vertex()
        self.get_graph().set_actor(oldVertex.get_id(), newVertex)
        self.vertex_observer_copy(oldVertex, newVertex)

    @interactionMask(OAGIS.EDITIONLEVELLOCK_1)
    def vertex_set_caption(self):
        """ Open a input dialog to set node caption """

        n = self.vertexItem().vertex()
        (result, ok) = QtGui.QInputDialog.getText(None, "Node caption", "",
                                   QtGui.QLineEdit.Normal, n.caption)
        if(ok):
            n.caption = str(result) #I HATE PROPERTIES, REALLY!

    @interactionMask(OAGIS.EDITIONLEVELLOCK_1)
    def vertex_show_hide_ports(self):
        """ Open port show/hide dialog """
        editor = ShowPortDialog(self.vertexItem().vertex(), self.get_graph_view())
        editor.exec_()

    @interactionMask(OAGIS.EDITIONLEVELLOCK_2)
    def vertex_mark_user_app(self, val):
        self.get_graph().set_continuous_eval(self.vertexItem().vertex().get_id(), bool(val))

    @interactionMask(OAGIS.EDITIONLEVELLOCK_2)
    def vertex_set_lazy(self, val):
        self.vertexItem().vertex().lazy = val #I DO HATE PROPERTIES, REALLY!

    @interactionMask(OAGIS.EDITIONLEVELLOCK_1)
    def vertex_block(self, val):
        self.vertexItem().vertex().block = val #I DEFINITELY DO HATE PROPERTIES, REALLY!

    @interactionMask(OAGIS.EDITIONLEVELLOCK_1)
    def vertex_edit_internals(self):
        """ Edit node internal data """
        editor = DictEditor(self.vertexItem().vertex().internal_data, self.get_graph_view())
        ret = editor.exec_()

        if(ret):
            for k in editor.modified_key:
                self.vertexItem().vertex().set_data(k, editor.pdict[k])
