import os, sys
pj = os.path.join

from setuptools import setup, find_packages

external_dependencies = [
'numpy>=1.3.0',
'scipy >= 0.7',
'matplotlib==0.98.5',
'PIL<=1.1.6',
'qt4>=4.5.2'
]

alea_dependencies = [
'openalea.deploy >= 0.7.dev',
'openalea.deploygui >= 0.7.dev',
'openalea.core >= 0.7.dev',
'openalea.visualea >= 0.7.dev',
'openalea.stdlib >= 0.7.dev',
'openalea.sconsx >=0.7.0.dev',
'openalea.misc >=0.7.0.dev',
'openalea.scheduler >=0.7.0.dev',
]

install_requires = alea_dependencies
if sys.platform.startswith('win'):
    install_requires += external_dependencies 

setup(
    name = 'OpenAlea',
    version = '0.7.0' ,
    description = 'OpenAlea packages and all its dependencies.', 
    long_description = '',
    author = 'OpenAlea consortium',
    author_email = 'christophe dot pradal at cirad dot fr',
    url = 'http://openalea.gforge.inria.fr',
    license = 'Cecill-C',


    create_namespaces=False,
    zip_safe=False,

    packages=find_packages('src'),

    package_dir={"":"src" },

    # Add package platform libraries if any
    include_package_data=True,

    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = install_requires,
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    # entry_points
    entry_points = {"wralea": ['openalea = openalea']},
    )


