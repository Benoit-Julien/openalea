#Check dependencies

import os, sys
pj= os.path.join

try:
    from openalea import config
except ImportError:
    print """
ImportError : openalea.config not found. 
Please install the openalea package before.	
See http://openalea.gforge.inria.fr
"""
    sys.exit()

from distutils.core import setup


# Package name
name= 'library'

namespace=config.namespace 
pkg_name= namespace + '.' + name
version= '0.1.0' 
description= 'OpenAlea Component platform library.' 

long_description= ''

author= 'OpenAlea consortium'
author_email= 'samuel.dufour@sophia.inria.fr, christophe.pradal@cirad.fr'

url= 'http://openalea.gforge.inria.fr'

license= 'Cecill-C' 


setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    
    packages= [ pkg_name ],
    package_dir= { pkg_name : pj('src',name)},

                     
    )


