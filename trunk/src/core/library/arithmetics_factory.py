# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Wralea for Core.Library 
"""

__license__= "Cecill-C"
__revision__=" $Id$ "



from openalea.core.core import NodeFactory


def define_factory(package):
    """ Define factories for arithmetics nodes """

    nf = NodeFactory( name= "add", 
                      description= "Addition", 
                      category = "Operations", 
                      nodemodule = "arithmetics",
                      nodeclass = "Add",
                      widgetmodule = None,
                      widgetclass = None, 
                      )

    package.add_nodefactory( nf )


    nf = NodeFactory( name= "sub", 
                      description= "Substration",
                      category = "Operations", 
                      nodemodule = "arithmetics",
                      nodeclass = "Sub", 
                      widgetmodule = None,
                      widgetclass = None,
                      )

    package.add_nodefactory( nf )


    nf = NodeFactory( name= "mult", 
                      description= "Multiplication",
                      category = "Operations",
                      nodemodule = "arithmetics",
                      nodeclass = "Mult",
                      widgetmodule = None,
                      widgetclass = None,
                      )

    package.add_nodefactory( nf )


    nf = NodeFactory( name= "div",
                      description= "Division", 
                      category = "Operations",
                      nodemodule = "arithmetics",
                      nodeclass = "Div",
                      widgetmodule = None,
                      widgetclass = None,
                      )

    package.add_nodefactory( nf )


    nf = NodeFactory( name = "val",
                      description = "Value",
                      category  = "Operations",
                      nodemodule = "arithmetics",
                      nodeclass = "Value",
                      widgetmodule = None,
                      widgetclass = None,
                      )

                      
    package.add_nodefactory( nf )

