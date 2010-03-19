# -*- python -*-
# -*- coding: latin-1 -*-
#
#       basics : numpy package
#
#       Copyright 2006 - 2010 INRIA - CIRAD - INRA  
#
#       File author(s): Eric MOSCARDI <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################


__doc__ = """ openalea.numpy """
__revision__ = " $Id: $ "


__name__ = "openalea.numpy.basics"
__alias__ = ["numpy.basics"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Numpy wrapping and utils module.'
__url__ = 'http://openalea.gforge.inria.fr'

__all__ = []

from openalea.core import Factory
from openalea.core.interface import *

list_type = ['bool', 'uint8', 'uint16', 'uint32', 'uint64', 'int8', 'int16', 'int32', 'int64', 'float32', 'float64', 'float96', 'complex64', 'complex128', 'complex192']

array = Factory(name= "array", 
              	description= "Create an array", 
              	category = "numpy",
		inputs = ( dict(name='object', interface=ISequence),
        		   dict(name='dtype', 
				interface=IEnumStr(list_type),
                       		value='float64'),
			   dict(name='copy', interface= IBool,
				value=True),
			   dict(name='order', interface=IEnumStr(['C', 'F', 'A']),
				value='C'),
			   dict(name='subok', interface= IBool,
				value=False),
			   dict(name='ndmin', interface= IInt,
				value=0),),
        	outputs = (dict(name='array', interface=ISequence),),
              	nodemodule = "basics",
              	nodeclass = "array",
               )

__all__.append("array")


zeros = Factory(name= "zeros", 
              	description= "Return a new array of given shape and type, filled with zeros", 
              	category = "numpy",
		inputs = ( dict(name='shape', interface=ISequence),
        		   dict(name='dtype', interface=IEnumStr(list_type), 
                       		value='float64'),
			   dict(name='order', interface=IEnumStr(['C', 'F']),
				value='C'),),
        	outputs = (dict(name='array', interface=ISequence),), 
              	nodemodule = "numpy",
              	nodeclass = "zeros",
               )

__all__.append("zeros")

ones = Factory(name= "ones", 
              	description= "Return a new array of given shape and type, filled with ones", 
              	category = "numpy",
		inputs = ( dict(name='shape', interface=ISequence),
        		   dict(name='dtype', interface=IEnumStr(list_type), 
                       		value='float64'),
			   dict(name='order', interface=IEnumStr(['C', 'F']),
				value='C'),),
        	outputs = (dict(name='array', interface=ISequence),), 
              	nodemodule = "numpy",
              	nodeclass = "ones",
               )

__all__.append("ones")

empty = Factory(name= "empty", 
              	description= "Return a new array of given shape and type, filled with ones", 
              	category = "numpy",
		inputs = ( dict(name='shape', interface=ISequence),
        		   dict(name='dtype', interface=IEnumStr(list_type), 
                       		value='float64'),
			   dict(name='order', interface=IEnumStr(['C', 'F']),
				value='C'),),
        	outputs = (dict(name='array', interface=ISequence),), 
              	nodemodule = "numpy",
              	nodeclass = "empty",
               )

__all__.append("empty")

arange = Factory(name= "arange", 
              	description= "Return evenly spaced values within a given interval", 
              	category = "numpy",
		inputs = ( dict(name='start', interface=IFloat, 
				value=0),
        		   dict(name='stop', interface=IFloat,
				value=0),
        		   dict(name='step', interface=IFloat,
				value=1),
			   dict(name='dtype', interface=IEnumStr(list_type), 
                       		value='float64'),),
        	outputs = (dict(name='array', interface=ISequence),), 
              	nodemodule = "numpy",
              	nodeclass = "arange",
               )

__all__.append("arange")

linspace = Factory(name= "linspace", 
              	description= "Return evenly spaced numbers over a specified interval", 
              	category = "numpy",
		inputs = ( dict(name='start', interface=IFloat, 
				value=0),
        		   dict(name='stop', interface=IFloat,
				value=0),
        		   dict(name='num', interface=IFloat,
				value=50),
        		   dict(name='endpoint', interface=IBool,
				value=True),
        		   dict(name='retstep', interface=IBool,
				value=True),),
        	outputs = (dict(name='samples', interface=ISequence), 
        		   dict(name='step', interface=IFloat),), 
              	nodemodule = "numpy",
              	nodeclass = "linspace",
               )

__all__.append("linspace")
