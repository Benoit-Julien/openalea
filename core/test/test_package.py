__license__ = "Cecill-C"
__revision__ = " $Id: test_package.py 1586 2009-01-30 15:56:25Z cokelaer $ "

from openalea.core.package import *
from openalea.core.node import gen_port_list
import os


def test_package():
    """Test package"""
    metainfo = {'version': '0.0.1',
              'license': 'CECILL-C',
              'authors': 'OpenAlea Consortium',
              'institutes': 'INRIA/CIRAD',
              'description': 'Base library.',
              'url': 'http://openalea.gforge.inria.fr',
              'icon': ''}

    package = Package("Test", metainfo)
    assert package != None


def test_userpackage():
    """Test user package"""
    metainfo = {'version': '0.0.1',
              'license': 'CECILL-C',
              'authors': 'OpenAlea Consortium',
              'institutes': 'INRIA/CIRAD',
              'description': 'Base library.',
              'url': 'http://openalea.gforge.inria.fr',
              'icon': ''}
    try:
        import shutil
        shutil.rmtree("tstpkg")
    except:
        pass

    assert not os.path.exists("tstpkg")

    try:
        os.mkdir("tstpkg")
    except:
        pass

    path = os.path.join(os.path.curdir, "tstpkg")
    package = UserPackage("DummyPkg", metainfo, path)


    factory = package.create_user_node("TestFact",\
         "category test", "this is a test",
                                       gen_port_list(3),
                                       gen_port_list(2))
    assert path in factory.search_path
    assert len(factory.inputs)==3
    assert len(factory.outputs)==2

    assert os.path.exists("tstpkg/TestFact.py")
    execfile("tstpkg/TestFact.py")

    package.write()
    assert os.path.exists("tstpkg/__wralea__.py")
    assert os.path.exists("tstpkg/__init__.py")
    execfile("tstpkg/__wralea__.py")

    # Test_clone_package
    path = os.path.join(os.path.curdir, "clonepkg")
    pkg2 = UserPackage("ClonePkg", metainfo, path)
    print pkg2.wralea_path

    pkg2.clone_from_package(package)
    pkg2.write()

    assert len(pkg2) == 1
    assert len(pkg2["TestFact"].inputs) == 3
    assert id(pkg2["TestFact"]) != id(package["TestFact"])
    assert os.path.exists(path)
    assert os.path.exists(os.path.join(path, '__wralea__.py'))
    assert os.path.exists(os.path.join(path, '__init__.py'))
    assert os.path.exists(os.path.join(path, 'TestFact.py'))
