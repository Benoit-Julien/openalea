# -*- python -*-
# -*- coding: latin-1 -*-
#
#       infos : numpy package
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


__name__ = "openalea.numpy.infos"
__alias__ = ["numpy.infos"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Numpy wrapping and utils module.'
__url__ = 'http://openalea.gforge.inria.fr'

__all__ = []

from openalea.core import Factory
from openalea.core.interface import *


ndim = Factory( name = "ndim", 
                description = "Number of array dimensions", 
                category = "numpy",
	        inputs = (dict(name='array', interface=ISequence),),
		outputs = (dict(name='ndim', interface= IInt),),
                nodemodule = "numpy",
                nodeclass = "ndim",
              )

__all__.append("ndim")


shape = Factory(name = "shape",
		description = "Tuple of array dimensions",
		category = "numpy",
		inputs = (dict(name='array', interface=ISequence),),
		outputs = (dict(name='shape', interface= ITuple3),),
                nodemodule = "numpy",
		nodeclass = "shape",
		)

__all__.append("shape")


size = Factory(name = "size",
		description = "Number of elements in the array",
		category = "numpy",
		inputs = (dict(name='array', interface=ISequence),),
		outputs = (dict(name='size', interface= IInt),),
                nodemodule = "numpy",
		nodeclass = "size",
		)

__all__.append("size")


dtype = Factory(name = "dtype",
		description = "Number of elements in the array",
		category = "numpy",
		inputs = (dict(name='array', interface=ISequence),),
		outputs = (dict(name='dtype', interface= IInt),),
                nodemodule = "numpy",
		nodeclass = "dtype",
		)

__all__.append("dtype")


itemsize = Factory(name = "itemsize",
		description = "The element size of this data-type object",
		category = "numpy",
		inputs = (dict(name='array', interface=ISequence),),
		outputs = (dict(name='itemsize', interface= IInt),),
                nodemodule = "numpy",
		nodeclass = "itemsize",
		)

__all__.append("itemsize")

