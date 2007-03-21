# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the CeCILL v2 License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
Default Node Widget and Subgraph Widget
"""

__license__= "CeCILL V2"
__revision__=" $Id$"



import sys
import math
import os

from PyQt4 import QtCore, QtGui
from openalea.core.core import NodeWidget
from openalea.core.interface import *


import types


class IInterfaceWidget(QtGui.QWidget, NodeWidget):
    """ Base class for widget associated to an interface """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """
        
        NodeWidget.__init__(self, node)
        QtGui.QWidget.__init__(self, parent)

        self.param_str = parameter_str

        self.update_state()


    def update_state(self):
        """ Enable or disable widget depending of connection status """

        i = self.node.get_input_index(self.param_str)
        state = self.node.get_input_state(i)
        
        if(state == "connected"):
            self.setEnabled(False)
        else:
            self.setEnabled(True)

    


class IFloatWidget(IInterfaceWidget):
    """
    Float spin box widget
    """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)
        
        hboxlayout = QtGui.QHBoxLayout(self)
        hboxlayout.setMargin(3)
        hboxlayout.setSpacing(5)

        self.label = QtGui.QLabel(self)
        self.label.setText(parameter_str)
        hboxlayout.addWidget(self.label)

        self.spin = QtGui.QDoubleSpinBox (self)
        self.spin.setRange(interface.min, interface.max)

        hboxlayout.addWidget(self.spin)

        self.notify(None,None)
        
        self.connect(self.spin, QtCore.SIGNAL("valueChanged(double)"), self.valueChanged)

        
    def valueChanged(self, newval):

        self.node.set_input_by_key(self.param_str, newval)
        
    def notify(self, sender, event):
        """ Notification sent by node """
        try:
            v = float(self.node.get_input_by_key(self.param_str))
        except:
            v = 0.
            print "FLOAT SPIN : cannot set value : ", self.node.get_input_by_key(self.param_str)

            
        self.spin.setValue(v)
        

class IIntWidget(IInterfaceWidget):
    """
    integer spin box widget
    """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        hboxlayout = QtGui.QHBoxLayout(self)
        hboxlayout.setMargin(3)
        hboxlayout.setSpacing(5)


        self.label = QtGui.QLabel(self)
        self.label.setText(parameter_str)
        hboxlayout.addWidget(self.label)

        self.spin = QtGui.QSpinBox (self)
        self.spin.setRange(interface.min, interface.max)

        hboxlayout.addWidget(self.spin)

        self.notify(None,None)

        self.connect(self.spin, QtCore.SIGNAL("valueChanged(int)"), self.valueChanged)

        
    def valueChanged(self, newval):

        self.node.set_input_by_key(self.param_str, newval)
        
        
    def notify(self, sender, event):
        """ Notification sent by node """

        try:
            v = int(self.node.get_input_by_key(self.param_str))
        except:
            v = 0
            print "INT SPIN : cannot set value : ", self.node.get_input_by_key(self.param_str)

        self.spin.setValue(v)



class IBoolWidget(IInterfaceWidget):
    """
    integer spin box widget
    """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        hboxlayout = QtGui.QHBoxLayout(self)
        hboxlayout.setMargin(3)
        hboxlayout.setSpacing(5)

        self.checkbox = QtGui.QCheckBox (parameter_str, self)

        hboxlayout.addWidget(self.checkbox)

        self.notify(node, None)
        self.connect(self.checkbox, QtCore.SIGNAL("stateChanged(int)"), self.stateChanged)

        
    def stateChanged(self, state):

        if(state == QtCore.Qt.Checked):
            self.node.set_input_by_key(self.param_str, True)
        else:
            self.node.set_input_by_key(self.param_str, False)
        
        
    def notify(self, sender, event):
        """ Notification sent by node """

        try:
            ischecked = bool(self.node.get_input_by_key(self.param_str))
        except:
            ischecked = False

        if(ischecked):
            self.checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkbox.setCheckState(QtCore.Qt.Unchecked)


class IStrWidget(IInterfaceWidget):
    """
    Line Edit widget
    """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtGui.QHBoxLayout(self)

        self.hboxlayout.setMargin(3)
        self.hboxlayout.setSpacing(5)


        self.label = QtGui.QLabel(self)
        self.label.setText(parameter_str)
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtGui.QLineEdit (self)
        self.hboxlayout.addWidget(self.subwidget)

        self.subwidget.setText(str(self.node.get_input_by_key(self.param_str)))

        self.connect(self.subwidget, QtCore.SIGNAL("textChanged(QString)"), self.valueChanged)

        
    def valueChanged(self, newval):

        self.node.set_input_by_key(self.param_str, str(newval))
        
        
    def notify(self, sender, event):
        """ Notification sent by node """

        self.subwidget.setText(str(self.node.get_input_by_key(self.param_str)))
        

class ISequenceWidget(IInterfaceWidget):
    """
    List edit widget
    """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtGui.QVBoxLayout(self)

        self.hboxlayout.setMargin(3)
        self.hboxlayout.setSpacing(5)


        self.label = QtGui.QLabel(self)
        self.label.setText(parameter_str)
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtGui.QListWidget (self)
        self.hboxlayout.addWidget(self.subwidget)

        self.button = QtGui.QPushButton("Add Item", self)
        self.hboxlayout.addWidget(self.button)

        self.update_list()
        self.connect(self.subwidget, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"),
                     self.itemclick)
        self.connect(self.subwidget, QtCore.SIGNAL("itemChanged(QListWidgetItem*)"),
                     self.itemchanged)
        self.connect(self.button, QtCore.SIGNAL("clicked()"), self.button_clicked)
        

    def update_list(self):

        seq = self.node.get_input_by_key(self.param_str)
        self.subwidget.clear()
        for elt in seq :
            item = QtGui.QListWidgetItem(str(elt))
            item.setFlags(QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled|
                          QtCore.Qt.ItemIsSelectable)
            self.subwidget.addItem(item)

    def button_clicked(self):
        seq = self.node.get_input_by_key(self.param_str)
        seq.append(None)
        self.update_list()
        
    def itemclick(self, item):
        self.subwidget.editItem(item)

    def itemchanged(self, item):
        text = item.text()
        i = self.subwidget.currentRow()
        seq = self.node.get_input_by_key(self.param_str)
        
        try:
            obj = eval(str(text))
            seq[i] = obj
            item.setText(str(obj))
        except :
            item.setText(text)
            seq[i] = str(text)
            
    def keyPressEvent(self, e):
        key   = e.key()
        seq = self.node.get_input_by_key(self.param_str)
        if( key == QtCore.Qt.Key_Delete):
            selectlist = self.subwidget.selectedItems()
            for i in selectlist:
                row = self.subwidget.row(i)
                self.subwidget.takeItem(row)
                del(seq[row-1])


    def notify(self, sender, event):
        """ Notification sent by node """
        self.update_list()


class IDictWidget(IInterfaceWidget):
    """
    List edit widget
    """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtGui.QVBoxLayout(self)

        self.hboxlayout.setMargin(3)
        self.hboxlayout.setSpacing(5)


        self.label = QtGui.QLabel(self)
        self.label.setText(parameter_str)
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtGui.QListWidget (self)
        self.hboxlayout.addWidget(self.subwidget)

        self.button = QtGui.QPushButton("Add Item", self)
        self.hboxlayout.addWidget(self.button)

        self.update_list()
        self.connect(self.subwidget, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"),
                     self.itemclick)
        self.connect(self.subwidget, QtCore.SIGNAL("itemChanged(QListWidgetItem*)"),
                     self.itemchanged)
        self.connect(self.button, QtCore.SIGNAL("clicked()"), self.button_clicked)
        

    def update_list(self):

        seq = self.node.get_input_by_key(self.param_str)
        self.subwidget.clear()
        for elt in seq :
            item = QtGui.QListWidgetItem(str(elt))
            item.setFlags(QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled|
                          QtCore.Qt.ItemIsSelectable)
            self.subwidget.addItem(item)

    def button_clicked(self):
        seq = self.node.get_input_by_key(self.param_str)
        seq.append(None)
        self.update_list()
        
    def itemclick(self, item):
        self.subwidget.editItem(item)

    def itemchanged(self, item):
        text = item.text()
        i = self.subwidget.currentRow()
        seq = self.node.get_input_by_key(self.param_str)
        
        try:
            obj = eval(str(text))
            seq[i] = obj
            item.setText(str(obj))
        except :
            item.setText(text)
            seq[i] = str(text)
            
    def keyPressEvent(self, e):
        key   = e.key()
        seq = self.node.get_input_by_key(self.param_str)
        if( key == QtCore.Qt.Key_Delete):
            selectlist = self.subwidget.selectedItems()
            for i in selectlist:
                row = self.subwidget.row(i)
                self.subwidget.takeItem(row)
                del(seq[row-1])


    def notify(self, sender, event):
        """ Notification sent by node """
        self.update_list()

        

class IFileStrWidget(IStrWidget):
    """
    File name Line Edit Widget
    """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IStrWidget.__init__(self, node, parent, parameter_str, interface)

        self.last_result= QtCore.QDir.homePath()
        self.button = QtGui.QPushButton("...", self)
        self.hboxlayout.addWidget(self.button)

        self.connect(self.button, QtCore.SIGNAL("clicked()"), self.button_clicked)

    def button_clicked(self):
        
        result = QtGui.QFileDialog.getOpenFileName(self, "Select File", self.last_result )
    
        if(result):
            self.node.set_input_by_key(self.param_str, str(result))
            self.last_result= result
            
        
class IEnumStrWidget(IInterfaceWidget):
    """ String Enumeration widget """
    
    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)
                
        self.hboxlayout = QtGui.QHBoxLayout(self)
        self.hboxlayout.setMargin(3)
        self.hboxlayout.setSpacing(5)

        self.label = QtGui.QLabel(self)
        self.label.setText(parameter_str)
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtGui.QComboBox(self)

        # map between string and combobox index
        self.map_index = {}
        for s in  interface.enum:
            self.subwidget.addItem(s)
            self.map_index[s] = self.subwidget.count() - 1
        
        self.hboxlayout.addWidget(self.subwidget)

        
        self.connect(self.subwidget,
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.valueChanged)

        
    def valueChanged(self, newval):
        self.node.set_input_by_key(self.param_str, str(newval))
        
        
    def notify(self, sender, event):
        """ Notification sent by node """

        strvalue = str(self.node.get_input_by_key(self.param_str))
        try:
            index = self.map_index[strvalue]
        except :
            index = -1

        self.subwidget.setCurrentIndex(index)



class IRGBColorWidget(IInterfaceWidget):
    """ RGB Color Widget """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtGui.QHBoxLayout(self)
        self.hboxlayout.setMargin(3)
        self.hboxlayout.setSpacing(5)

        self.label = QtGui.QLabel(self)
        self.label.setText(parameter_str)
        self.hboxlayout.addWidget(self.label)

        self.colorwidget = QtGui.QWidget(self)
        self.colorwidget.setAutoFillBackground(True)

        self.colorwidget.setMinimumSize(QtCore.QSize(50,50))
        self.colorwidget.setBackgroundRole(QtGui.QPalette.Window)
        self.colorwidget.mouseDoubleClickEvent = self.widget_clicked
        self.notify(node, None)
        
        self.hboxlayout.addWidget(self.colorwidget)


    def widget_clicked(self,event):
        
        try:
            (r,g,b) = self.node.get_input_by_key(self.param_str)
            oldcolor = QtGui.QColor(r,g,b)
        except:
            oldcolor = QtCore.Qt.White                                        
        
        color = QtGui.QColorDialog.getColor(oldcolor, self)
    
        if(color):
            self.node.set_input_by_key(self.param_str, (color.red(), color.green(), color.blue()))

    def notify(self, sender, event):
        """ Notification sent by node """

        try:
            (r,g,b) = self.node.get_input_by_key(self.param_str)
        except:
            (r,g,b) = (0,0,0)
        
        palette = self.colorwidget.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(r,g,b))
        self.colorwidget.setPalette(palette)
        self.colorwidget.update()
        
  

   

class DefaultNodeWidget(NodeWidget, QtGui.QWidget):
    """
    Default implementation of a NodeWidget.
    It displays the node contents.
    """

    # Map between type and widget
    type_map= {IFloat: IFloatWidget,
               IInt : IIntWidget,
               IStr : IStrWidget,
               IFileStr: IFileStrWidget,
               IBool : IBoolWidget,
               IEnumStr : IEnumStrWidget,
               IRGBColor : IRGBColorWidget,
               IDict : IDictWidget,
               ISequence : ISequenceWidget,
               types.NoneType : None
              }
    

    def __init__(self, node, parent):

        NodeWidget.__init__(self, node)
        QtGui.QWidget.__init__(self, parent)
        self.setMinimumSize(100, 20)

        self.widgets = []

        vboxlayout = QtGui.QVBoxLayout(self)
        vboxlayout.setMargin(3)
        vboxlayout.setSpacing(2)

        empty = True
        for (name, interface) in node.input_desc:

            if(type(interface) == types.TypeType):
                interface = interface()
            
            wclass= self.type_map.get(interface.__class__,None)

            if(wclass):
                widget = wclass(node, self, name, interface)
                vboxlayout.addWidget(widget)
                self.widgets.append(widget)
                empty = False
            else:
                self.widgets.append(None)

        # If there is no subwidget, add the name
        if( empty):
            label = QtGui.QLabel(self)
            label.setText(self.node.__class__.__name__+
                          " (No Widget available)")

            vboxlayout.addWidget(label)

    
    def notify(self, sender, event):
        """ Function called by observed objects """

        if(event and event[0] == "input_modified"):
            input_index = event[1]

            widget= self.widgets[input_index]
            if widget: 
                widget.notify(sender, event)
                widget.update_state()
