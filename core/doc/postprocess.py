""" clean up tool

The reST files are automatically generated using sphinx_tools.

However, there are known issus which require cleaning.

This code is intended at cleaning these issues until a neat 
solution is found.
"""
import os
import sys
from openalea.misc import sphinx_tools


filenames = [   'core/openalea_clonepkg_TestFact_src.rst',
                'core/openalea_tstpkg_TestFact_ref.rst', 
                'core/openalea_tstpkg_TestFact_src.rst',
                'core/openalea_clonepkg_TestFact_ref.rst']

for file in filenames:
    try:
        process = sphinx_tools.PostProcess(file)
        process.remove_file()
    except:pass


print 'Try python setup.py build_sphinx now.'

