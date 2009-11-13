# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
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
################################################################################
"""QT4 Main window"""

__license__ = "CeCILL v2"
__revision__ = " $Id$ "


from PyQt4 import QtCore, QtGui, QtSvg
from PyQt4.QtCore import SIGNAL

import ui_mainwindow
from openalea.visualea.shell import get_shell_class

from openalea.core import cli
from code import InteractiveInterpreter as Interpreter

from openalea.visualea.node_treeview import NodeFactoryTreeView, PkgModel, CategoryModel
from openalea.visualea.node_treeview import DataPoolListView, DataPoolModel
from openalea.visualea.node_treeview import SearchListView, SearchModel
from openalea.visualea.node_widget import SignalSlotListener
import metainfo


from openalea.visualea.dialogs import NewGraph, NewPackage
from openalea.visualea.dialogs import PreferencesDialog, NewData

from openalea.grapheditor import qtgraphview
from graph_operator import GraphOperator
import visualea_integration

class MainWindow(QtGui.QMainWindow,
                 ui_mainwindow.Ui_MainWindow,
                 SignalSlotListener) :

    def __init__(self, session, parent=None):
        """        
        @param session : user session
        @param parent : parent window
        """

        QtGui.QMainWindow.__init__(self, parent)
        SignalSlotListener.__init__(self)
        ui_mainwindow.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.setAttribute(QtCore.Qt.WA_QuitOnClose)
        self.pkgmanager = session.pkgmanager

        # Set observer
        self.initialise(session)

        self.tabWorkspace.removeTab(0)
        #self.tabWorkspace.setTabsClosable(True)
        self.ws_cpt = 0

        # python interpreter
        interpreter = Interpreter()
        cli.init_interpreter(interpreter, session)
        shellclass = get_shell_class()
        self.interpreterWidget = shellclass(interpreter,
                                            cli.get_welcome_msg(),
                                            parent=self.splitter)

        # package tree view
        self.pkg_model = PkgModel(self.pkgmanager)
        self.packageTreeView = \
            NodeFactoryTreeView(self, self.packageview)
        self.packageTreeView.setModel(self.pkg_model)
        self.vboxlayout1.addWidget(self.packageTreeView)

        # category tree view
        self.cat_model = CategoryModel(self.pkgmanager)
        self.categoryTreeView = \
            NodeFactoryTreeView(self, self.categoryview)
        self.categoryTreeView.setModel(self.cat_model)
        self.vboxlayout2.addWidget(self.categoryTreeView)

        # search list view
        self.search_model = SearchModel()
        self.searchListView = \
            SearchListView(self, self.searchview)
        self.searchListView.setModel(self.search_model)
        self.vboxlayout3.addWidget(self.searchListView)


        # data pool list view
        self.datapool_model = DataPoolModel(session.datapool)
        self.datapoolListView = \
            DataPoolListView(self, session.datapool, self.pooltab)
        self.datapoolListView.setModel(self.datapool_model)
        self.vboxlayout4.addWidget(self.datapoolListView)

        # use view
      #   self.datapoolListView2 = DataPoolListView(self, session.datapool, self.usetab)
#         self.datapoolListView2.setModel(self.datapool_model)
#         self.vboxlayout5.addWidget(self.datapoolListView2)

        # Widgets
        self.connect(self.tabWorkspace, SIGNAL("contextMenuEvent(QContextMenuEvent)"),
                     self.contextMenuEvent)
        self.connect(self.tabWorkspace, SIGNAL("currentChanged(int)"), self.ws_changed)
        self.connect(self.search_lineEdit, SIGNAL("editingFinished()"), self.search_node)
        self.connect(self.tabWorkspace, SIGNAL("tabCloseRequested(int)"),
                     self.close_tab_workspace)


        # Help Menu
        self.connect(self.action_About, SIGNAL("triggered()"), self.about)
        self.connect(self.actionOpenAlea_Web, SIGNAL("triggered()"), self.web)
        self.connect(self.action_Help, SIGNAL("triggered()"), self.help)

        # File Menu
        self.connect(self.action_New_Session, SIGNAL("triggered()"),\
                     self.new_session)
        self.connect(self.action_Open_Session, SIGNAL("triggered()"),\
                     self.open_session)
        self.connect(self.action_Save_Session, SIGNAL("triggered()"),\
                     self.save_session)
        self.connect(self.actionSave_as, SIGNAL("triggered()"), self.save_as)
        self.connect(self.action_Quit, SIGNAL("triggered()"), self.quit)
        
        self.connect(self.action_Image, SIGNAL("triggered()"), self.export_image)
        self.connect(self.action_Svg, SIGNAL("triggered()"), self.export_image_svg)

        # Package Manager Menu
        self.connect(self.action_Auto_Search, SIGNAL("triggered()"), self.reload_all)
        self.connect(self.action_Add_File, SIGNAL("triggered()"), self.add_pkgdir)
        self.connect(self.actionFind_Node, SIGNAL("triggered()"),
                     self.find_node)
        self.connect(self.action_New_Network, SIGNAL("triggered()"), self.new_graph)
        self.connect(self.actionNew_Python_Node, SIGNAL("triggered()"), self.new_python_node)
        self.connect(self.actionNew_Package, SIGNAL("triggered()"), self.new_package)
        self.connect(self.action_Data_File, SIGNAL("triggered()"), self.new_data)
        self.connect(self.actionShow_log, SIGNAL("triggered()"), self.pkgmanager.log.print_log)
        
        # DataPool Menu
        self.connect(self.actionClear_Data_Pool, SIGNAL("triggered()"), self.clear_data_pool)

        # Python Menu
        self.connect(self.action_Execute_script, SIGNAL("triggered()"),
                     self.exec_python_script)
        self.connect(self.actionOpen_Console, SIGNAL("triggered()"),
                     self.open_python_console)
        self.connect(self.actionClea_r_Console, SIGNAL("triggered()"),
                     self.clear_python_console)

        
        # WorkspaceMenu 
        # daniel was here: now the menu is built using the graph operator.
        self.operator = None
        QtCore.QObject.connect(self.menu_Workspace, 
                               QtCore.SIGNAL("aboutToShow()"), 
                               self.__wsMenuShow)
        QtCore.QObject.connect(self.menu_Workspace, 
                               QtCore.SIGNAL("aboutToHide()"), 
                               self.__wsMenuHide)
        QtCore.QObject.connect(self.action_New_Empty_Workspace,
                               QtCore.SIGNAL("triggered()"), 
                               self.new_workspace)
                


        # Window Mneu
        self.connect(self.actionPreferences, SIGNAL("triggered()"), self.open_preferences)
        self.connect(self.actionDisplay_Package_Manager, SIGNAL("toggled(bool)"), 
                     self.display_leftpanel)
        self.connect(self.actionDisplay_Workspaces, SIGNAL("toggled(bool)"), 
                     self.display_rightpanel)
                
        self.setAcceptDrops(True)
        # final init
        self.session = session

        self.session.simulate_workspace_addition()

    
    def __wsMenuShow(self):
        widget = self.tabWorkspace.currentWidget()
        if widget is None:
            return

        operator = GraphOperator(widget, widget.graph())
        operator.set_session(self.session)
        operator.set_interpreter(self.interpreterWidget)
        operator.set_package_manager(self.pkgmanager)
        operator.register_listener(self)

        menu = self.menu_Workspace
        menu.clear() #until i modify the ui files.

        menu.addAction(operator("Run", menu, "graph_run"))
        menu.addAction(operator("Reset", menu, "graph_reset"))
        menu.addAction(operator("Invalidate", menu, "graph_invalidate"))
        menu.addSeparator()
        menu.addAction(operator("Copy", menu, "graph_copy"))
        menu.addAction(operator("Cut", menu, "graph_cut"))
        menu.addAction(operator("Paste", menu, "graph_paste"))
        menu.addSeparator()
        menu.addAction(operator("Remove selected vertices", menu, "graph_remove_selection"))
        menu.addAction(operator("Group selected vertices", menu, "graph_group_selection"))
        menu.addAction(operator("Change selection color", menu, "graph_set_selection_color"))
        menu.addSeparator()
        menu.addAction(self.action_New_Empty_Workspace)
        menu.addAction(operator("Close current workspace", menu, "graph_close"))
        menu.addAction(operator("Configure IO", menu, "graph_configure_io"))
        menu.addAction(operator("Reload workspace", menu, "graph_reload_from_factory"))
        menu.addAction(operator("Export to factory", menu, "graph_export_to_factory"))
        menu.addSeparator()
        menu.addAction(operator("Preview application", menu, "graph_preview_application"))
        menu.addAction(operator("Export to application", menu, "graph_export_application"))
        self.operator=operator #don't look! 
        
    def __wsMenuHide(self):
        if(self.operator):
            self.operator.unregister_listener(self)
            self.operator=None

    def open_compositenode(self, factory):
        """ open a  composite node editor """
        node = factory.instantiate()

        self.session.add_workspace(node, notify=False)
        self.open_widget_tab(node, factory=factory)


    def about(self):
        """ Display About Dialog """
        
        mess = QtGui.QMessageBox.about(self, "About Visualea",
                                       "Version %s\n\n"%(metainfo.get_version()) +
                                       "VisuAlea is part of the OpenAlea framework.\n"+
                                       metainfo.get_copyrigth()+
                                       "This Software is distributed under the Cecill-V2 License.\n\n"+
                                       "Visit " + metainfo.url +"\n\n"
                                       )

    def help(self):
        """ Display help """
        self.web()

    def web(self):
        """ Open OpenAlea website """
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(metainfo.url))


    def quit(self):
        """ Quit Application """

        QtGui.QApplication.closeAllWindows()


    def notify(self, sender, event):
        """ Notification from observed """
        if(event and event[0] == "graphoperator_newfactory"):
            self.reinit_treeview()
            return

        if(type(sender) == type(self.session)):
            
            if(event and event[0]=="workspace_added"):
                graph=event[1]
                self.open_widget_tab(graph, graph.factory)
            else:
                self.update_tabwidget()
                self.reinit_treev
    
    def closeEvent(self, event):
        """ Close All subwindows """
        
        for i in range(self.tabWorkspace.count()):
            w = self.tabWorkspace.widget(i)
            w.close()

        event.accept()

    
    def reinit_treeview(self):
        """ Reinitialise package and category views """

        self.cat_model.reset()
        self.pkg_model.reset()
        self.datapool_model.reset()
        self.search_model.reset()
                   

    def close_tab_workspace(self, cindex):
        """ Close workspace indexed by cindex cindex is Node"""
        
        w = self.tabWorkspace.widget(cindex)
        self.tabWorkspace.removeTab(cindex)
        w.close()

      
    def current_view (self) :
        """ Return the active widget """
        return self.tabWorkspace.currentWidget()
    
    def update_tabwidget(self):
        """ open tab widget """
        # open tab widgets
        for (i, node) in enumerate(self.session.workspaces):

            if(i< self.tabWorkspace.count()):
                widget = self.tabWorkspace.widget(i)
                if(node != widget.graph().graph()):
                    self.close_tab_workspace(i)
                self.open_widget_tab(node, factory=node.factory, pos = i)
            
        # close last tabs
        removelist = range( len(self.session.workspaces), self.tabWorkspace.count())
        removelist.reverse()
        for i in removelist:
            self.close_tab_workspace(i)


    def open_widget_tab(self, graph, factory, caption=None, pos = -1):
        """
        Open a widget in a tab giving an instance and its widget
        caption is append to the tab title
        """

        # Test if the node is already opened
        for i in range(self.tabWorkspace.count()):
            widget = self.tabWorkspace.widget(i)
            n = widget.graph().graph()
            if(graph is n):
                self.tabWorkspace.setCurrentIndex(i)
                return

        #gengraph
        gwidget = None
        try:
            gwidget = qtgraphview.QtGraphView(self, graph)
            gwidget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        except Exception, e:
            print "open_widget_tab", e
            pass
        #/gengraph

        if(not caption) :
            i = self.session.workspaces.index(graph)
            caption = "Workspace %i - %s"%(i, graph.get_caption())
        
        index = self.tabWorkspace.insertTab(pos, gwidget, caption)
        self.tabWorkspace.setCurrentIndex(index)

        return index
        

    def add_pkgdir(self):

        dirname = QtGui.QFileDialog.getExistingDirectory(self, "Select Package/Directory")
        if(dirname):
            self.pkgmanager.load_directory(str(dirname))
            self.reinit_treeview()

    
    def reload_all(self):

        # Reload package manager
        self.pkgmanager.reload()
        self.reinit_treeview()

        # Reload workspace
        for index in range(self.tabWorkspace.count()):
            self.reload_from_factory(index)
         
    
    def ws_changed(self, index):
        """ Current workspace has changed """
        self.session.cworkspace = index
        
            
    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""

        pos = self.tabWorkspace.mapFromGlobal(event.globalPos())
        
        tabBar = self.tabWorkspace.tabBar()
        count = tabBar.count()

        index = -1
        for i in range(count):
            if(tabBar.tabRect(i).contains(pos)):
                index = i
                break

        # if no bar was hit, return
        if (index<0):
            return 

        # set hit bar to front
        self.tabWorkspace.setCurrentIndex(index)
        
        def close_current_ws():
            self.close_tab_workspace(index)
        
        menu = QtGui.QMenu(self)

        action = menu.addAction("Close")
        self.connect(action, SIGNAL("triggered()"), close_current_ws)

#         action = menu.addAction("Run")
#         self.connect(action, SIGNAL("triggered()"), self.run)

#         action = menu.addAction("Export to Model")
#         self.connect(action, SIGNAL("triggered()"), self.export_to_factory)

        menu.move(event.globalPos())
        menu.show()

    def new_workspace(self):
        """ Create an empty workspace """
        self.session.add_workspace()

    def new_graph(self):
        """ Create a new graph """

        dialog = NewGraph("New Composite Node", self.pkgmanager, self)
        ret = dialog.exec_()

        if(ret>0):
            newfactory = dialog.create_cnfactory(self.pkgmanager)
            self.reinit_treeview()
            self.open_compositenode(newfactory)

    def new_python_node(self):
        """ Create a new node """

        dialog = NewGraph("New Python Node", self.pkgmanager, self)
        ret = dialog.exec_()

        if(ret>0):
            dialog.create_nodefactory(self.pkgmanager)
            self.reinit_treeview()

    def new_data(self):
        """ Import file """

        dialog = NewData("Import data file", self.pkgmanager, self)
        ret = dialog.exec_()

        if(ret>0):
            dialog.create_datafactory(self.pkgmanager)
            self.reinit_treeview()

    def new_package(self):
        """ Create a new user package """

        dialog = NewPackage(self.pkgmanager.keys(), parent = self)
        ret = dialog.exec_()

        if(ret>0):
            (name, metainfo, path) = dialog.get_data()

            self.pkgmanager.create_user_package(name, metainfo, path)
            self.reinit_treeview()
        
    def exec_python_script(self):
        """ Choose a python source and execute it """
            
        filename = QtGui.QFileDialog.getOpenFileName(
            self, "Python Script", "Python script (*.py)")

        filename = str(filename)
        if(not filename) : return

        import code
        file = open(filename, 'r')
        
        sources = ''
        compiled = None
        
        for line in file:
            sources += line
            compiled = code.compile_command(sources, filename)

            if(compiled):
                self.interpreterWidget.get_interpreter().runcode(compiled)
                sources = ''

    def open_python_console(self):
        """ Set focus on the python shell """
        self.interpreterWidget.setFocus(QtCore.Qt.ShortcutFocusReason)
    
    def clear_python_console(self):
        """ Clear python shell """
        self.interpreterWidget.clear()

    def new_session(self):
        self.session.clear()
       
    def open_session(self):

        filename = QtGui.QFileDialog.getOpenFileName(
            self, "OpenAlea Session", QtCore.QDir.homePath(), "Session file (*.oas)")

        filename = str(filename)
        if(not filename) : return

        self.session.load(filename)

    def save_session(self):
        """ Save menu entry """
        
        if(not self.session.session_filename):
            self.save_as()
        else :
            self.session.save(self.session.session_filename)

    def save_as(self):
        """ Save as menu entry """
        
        filename = QtGui.QFileDialog.getSaveFileName(
            self, "OpenAlea Session",  QtCore.QDir.homePath(), "Session file (*.oas)")

        filename = str(filename)
        if(not filename) : return

        self.session.save(filename)
        
    def clear_data_pool(self):
        """ Clear the data pool """

        self.session.datapool.clear()

    def search_node(self):
        """ Activated when search line edit is validated """

        results = self.pkgmanager.search_node(str(self.search_lineEdit.text()))
        self.search_model.set_results(results)
        
    def find_node(self):
        """ Find node Command """

        i = self.tabPackager.indexOf(self.searchview)
        self.tabPackager.setCurrentIndex(i)
        self.search_lineEdit.setFocus()

    def open_preferences(self):
        """ Open Preference dialog """

        dialog = PreferencesDialog(self)
        ret = dialog.exec_()
        # ! does not return anythin and do not use ret ? 

        
    # Drag and drop support 
    def dragEnterEvent(self, event):
        """todo"""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """todo"""
        urls = event.mimeData().urls()
        try:
            file = urls[0]
            filename = str(file.path())
            self.session.load(filename)
            event.accept()

        except Exception, e:
            print e
            event.ignore()

            
    # Window support
    def display_leftpanel(self, toggled):
        self.splitter_2.setVisible(toggled)
    

    def display_rightpanel(self, toggled):
        self.splitter.setVisible(toggled)


    def export_image(self):
        """ Export current workspace to an image """
        
        filename = QtGui.QFileDialog.getSaveFileName(
            self, "Export image",  QtCore.QDir.homePath(), "PNG Image (*.png)")

        filename = str(filename)
        if(not filename) : return
        
        # Get current workspace
        view = self.tabWorkspace.currentWidget()
        rect = view.scene().sceneRect()

        pixmap = QtGui.QPixmap(rect.width(), rect.height())
        pixmap.fill()
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        view.update()
        view.scene().render(painter)
        painter.end()
        pixmap.save(filename)

    def export_image_svg(self):
        """ Export current workspace to an image """
        
        filename = QtGui.QFileDialog.getSaveFileName(
            self, "Export svg image",  QtCore.QDir.homePath(), "SVG Image (*.svg)")

        filename = str(filename)
        if(not filename) : return
        
        # Get current workspace
        view = self.tabWorkspace.currentWidget()
        rect = view.scene().sceneRect()

        svg_gen = QtSvg.QSvgGenerator()
        svg_gen.setFileName(filename)
        svg_gen.setSize(rect.toRect().size())

        painter = QtGui.QPainter(svg_gen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        view.scene().render(painter, )
        painter.end()

        #pixmap.save(filename)

