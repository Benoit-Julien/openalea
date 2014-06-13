# -*- python -*-
#
#       OALab start here
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
import sys

from openalea.oalab.cli.parser import CommandLineParser
from openalea.oalab.project.symlink import create_project_shortcut
from openalea.oalab.session.all import Session

def main():
    """
    1. Parse command line arguments.
    2. If GUI enabled (session.gui), launch QApplication
    3. Search an extension in "oalab.extension" plugins.
        - If found, launch extension
        - If not found, quit application and shows available extensions
    """

    create_project_shortcut()

    session = Session()
    cli = CommandLineParser(sys.argv, session)

    if session.gui:
        from openalea.vpltk.qt import QtGui
        from openalea.oalab.gui.mainwindow import MainWindow
        from openalea.vpltk.plugin import iter_plugins

        app = QtGui.QApplication(sys.argv)

        win = None
        # Run all extension matching session.extension
        available_extensions = []
        for plugin in iter_plugins('oalab.lab', debug=session.debug_plugins):
            try:
                ext = plugin.name
            except AttributeError:
                continue
            else:
                # register plugin info for user.
                args = dict(EXT=ext, MODULE=plugin.__module__, CLASS=plugin.__name__)
                text = '  - \033[94m%(EXT)s\033[0m (provided by class %(CLASS)s defined in %(MODULE)s)' % args
                available_extensions.append(text)

            factory = plugin()
            if session.extension == ext:
                win = MainWindow(session)
                factory(win)
                win.show()
                win.raise_()

        if win:
            app.exec_()
        else:
            print 'Extension %r not found' % session.extension
            print 'Please choose a valid \033[94mextension\033[0m:'
            print '\n'.join(available_extensions)


if(__name__ == "__main__"):
    main()
