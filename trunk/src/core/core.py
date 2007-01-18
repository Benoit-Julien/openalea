# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
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
This module defines all the base class for the OpenAlea Kernel (Node, Package...)
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

###############################################################################


# Exceptions

class UnknownNodeError (Exception):
    pass


class RecursionError (Exception):
    pass

class InstantiationError(Exception):
    pass

###############################################################################

from observer import Observed, AbstractListener
import imp


class Node(Observed):
    """
    Base class for all Nodes.
    A Node is a callable object with typed inputs and outputs.
    """

    def __init__(self):

        # Effective values
        Observed.__init__(self)

        # Values
        self.inputs = []
        self.outputs = []

        # Description
        self.input_desc = []
        self.output_desc = []
        
        
        self.map_index_in = {}
        self.map_index_out = {}
        

        # Factory
        self.factory = None
        

    def __call__(self):
        """ Call function. Must be overriden """
        
        raise RuntimeError('Node function not implemented.')


    # Accessor
    
    def get_factory(self):
        return self.factory

    # Declarations
    def add_input(self, name, interface, value = None):
        """ Create an input port """

        self.inputs.append( value )
        self.input_desc.append( (name, interface) )
        self.map_index_in[name]= len(self.inputs) - 1


    def add_output(self, name, interface):
        """ Create an output port """

        self.outputs.append( None )
        self.output_desc.append( (name, interface) )
        self.map_index_out[name]= len(self.outputs) - 1


    # I/O Functions
    def get_input_interface_by_key(self, key):

        index = self.map_index_in[key]
        return self.input_desc[index][1]


    def get_output_interface_by_key(self, key):

        index = self.map_index_out[key]
        return self.output_desc[index][1]

    
    def get_input_by_key(self, key):

        index = self.map_index_in[key]
        return self.inputs[index]


    def set_input_by_key(self, key, val):

        index = self.map_index_in[key]
        self.inputs[index] =  val
        self.notify_listeners()


    def get_output_by_key(self, key):

        index = self.map_index_out[key]
        return self.outputs[index]


    def set_output_by_key(self, key, val):

        index = self.map_index_out[key]
        self.outputs[index] =  val

    
    def get_input(self, index):
        """ Return an input port value """

        return self.inputs[index]


    def set_input(self, index, val):
        """ Define the input value for the specified index """
        self.inputs[index] = val
        self.notify_listeners()


    def get_output(self, index):
        """ Return the output for the specified index """
        return self.outputs[index]


    def set_output(self, index, val):
        """ Define the output value for the specified index """
        self.outputs[index] = val

   
    def get_nb_input(self):
        return len(self.inputs)

    
    def get_nb_output(self):
        return len(self.outputs)

    
    # Functions used by the node evaluator
    def eval(self):
        """ Evaluate the node by calling __call__"""

        outlist = self.__call__(self.inputs)

        if(not isinstance(outlist, tuple) and
           not isinstance(outlist, list)):
            outlist = (outlist,)

        for i in range( min ( len(outlist), len(self.outputs))):
            self.outputs[i] = outlist[i]



###############################################################################


class NodeFactory(Observed):
    """
    A Node factory is able to create node on demand, and their associated widget.
    """

    mimetype = "openalea/nodefactory"

    def __init__(self,
                 name,
                 description = '',
                 category = '',
                 nodemodule = '',
                 nodeclass = None,
                 widgetmodule = None,
                 widgetclass = None,
                 parameters = [],
                 **kargs):
	"""
	Create a node factory.
	
	@param name : user name for the node (must be unique)
        @param description : description of the node
	@param category : category of the node
        @param nodemodule : 'python module to import for node'
	@param nodeclass :  node class name to be created
        @param widgetmodule : 'python module to import for widget'
	@param widgetclass : widget class name
        @param parameters : list of parameters name
	
	@type name : String
	@type description : String
	@type category : String
        @type nodemodule : String
	@type nodeclass : String
        @type widgetmodule : String
	@type widgetclass : String
        @type parameters : list of string
	"""

        Observed.__init__(self)
        
        self.name = name
        self.description = description
        self.category = category
        self.nodemodule = nodemodule
        self.nodeclass_name = nodeclass
        self.widgetmodule = widgetmodule
        self.widgetclass_name = widgetclass
        self.parameters = parameters

    def get_id(self):
        """ Return the node factory Id """
        return self.name


    def get_tip(self):
        """ Return the node description """

        return "Name : %s\n"%(self.name,) +\
               "Category  : %s\n"%(self.category,) +\
               "Description : %s\n"%(self.description,)


    def get_xmlwriter(self):
        """ Return an instance of a xml writer """

        from pkgreader import NodeFactoryXmlWriter
        return NodeFactoryXmlWriter(self)
        

    def instantiate(self, call_stack=[]):
        """ Return a node instance
        @param call_stack : the list of NodeFactory id already in call stack
        (in order to avoir infinite recursion)
        """

        if(self.nodemodule):
            try:
                (file, pathname, desc) = imp.find_module(self.nodemodule)
                module = imp.load_module(self.nodemodule, file, pathname, desc)
                if(file) : file.close()

                classobj = module.__dict__[self.nodeclass_name]
                node = classobj()
                
                node.factory = self
                return node
            
            except ImportError:
                raise InstantiationError()
    

    def instantiate_widget(self, node, parent=None):
        """ Return the corresponding widget initialised with node """

        if(node == None):
            node = self.instantiate()

        modulename = self.widgetmodule
        if(not modulename) :   modulename = self.nodemodule

        if(modulename and self.widgetclass_name):

            (file, pathname, desc) = imp.find_module(modulename)
            module = imp.load_module(modulename, file, pathname, desc)
            if(file) : file.close()

            widgetclass = module.__dict__[self.widgetclass_name]

            return widgetclass(node, parent)
        
        else:
            try:
                # if no widget declared, we create a default one
                from openalea.visualea.node_widget import DefaultNodeWidget
                return DefaultNodeWidget(node, parent)
            
            except ImportError:
                raise InstantiationError()


#class Factory:
   
Factory = NodeFactory


###############################################################################

class NodeWidget(AbstractListener):
    """
    Base class for all node widget classes
    """

    def __init__(self, node):

        self.node = node

        # register to observed node and factory
        self.initialise(node)
        self.initialise(node.get_factory())
            

    def get_node(self):
        return self.__node


    def set_node(self, node):
        self.__node = node


    def get_factory(self):
        return self.__node.get_factory()


    node = property(get_node, set_node)

    factory = property(get_factory)
    

    def notify(self):
        """
        This function is called by the Observed objects
        and must be overloaded
        """
        pass


###############################################################################

        

class Package(dict):
    """
    A Package is a dictionnary of node factory.
    Each node factory is able to generate node and their widget

    Meta informations are associated with a package.
    """

    mimetype = "openalea/package"


    def __init__(self, name, metainfo) :
	"""
        Create a Package

        @param name : a unique string that will be used as an unique identifier for the package
        @param metainfo : a dictionnary for metainformation. Attended keys are :
            license : a string ex GPL, LGPL, Cecill, Cecill-C
            version : a string
            authors : a string
            institutes : a string
            description : a string for the package description
            publication : optional string for publications
            
	"""

        dict.__init__(self)
        
        self.name = name
        self.metainfo = metainfo

        # association between node name and node factory
        #self.__node_factories = {}


    def get_id(self):
        """ Return the package id """
        return self.name


    def get_tip(self):
        """ Return the package description """

        str= "Package : %s\n"%(self.name,)
        try: str+= "Description : %s\n"%(self.metainfo['description'],)
        except : pass
        try: str+= "Institutes : %s\n"%(self.metainfo['institutes'],)
        except : pass 

        return str


    def get_metainfo(self, key):
        """Return a meta information. See the standard key the __init__ function documentation"""

        return self.metainfo[key]


    def add_factory(self, factory):
        """ Add to the package a factory ( node or subgraph ) """
        self[ factory.name ] = factory


    def get_names(self):
        """ Return all the factory names  in a list"""

        return self.keys()
    

    def get_factory(self, id):
        """ Return the factory associated with id """

        try:
            factory = self[id]
        except KeyError:
            raise UnknownNodeError()

        return factory


    def get_info(self, id):
        """ Return the tuple (name, category, description, doc) for the factory id """

        nf = self.get_factory(id)

        return (nf.name, nf.category, nf.description, nf.doc)

        


