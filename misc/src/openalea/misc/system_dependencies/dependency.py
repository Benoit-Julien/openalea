# -*- python -*-
#
#       VirtualPlant's buildbot continuous integration scripts.
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
###############################################################################

import platform, types, warnings, collections
import dependencies, os_factory


__all__ = ["Dependency", "EggDependency", "InstallerDependency"]


class DistributionPackageFactory(os_factory.BaseOsFactory):
    def __init__(self):
        self.__distPkgs = {}

    def register(self, cls):
        assert isinstance(type(cls), types.TypeType)
        name = cls.__name__
        name = name[:name.find("_PackageNames")].replace("_", " ").lower()
        print "registering:", name
        self.__distPkgs[name] = cls

    def create(self, platform=None, conflictSolve=lambda x: x[0]):
        assert platform is not None
        maxIntersectionDistrib = self.intersect_and_solve(platform, self.__distPkgs.keys(), conflictSolve)
        cls = self.__distPkgs.get(maxIntersectionDistrib, None)
        if cls: return cls()




# -- Decanonification and handling special package types like eggs --
class DistributionPackageNames(dict):
    """Base class for per-OS decanonification"""
    def __init__(self, **packages):
        dict.__init__(self)
        self.update(packages)
    def update(self, other):
        ks, vs = zip(*other.iteritems())
        other = dict(zip(ks,map(lambda x: BaseDependency(x) if isinstance(x,str) else x,
                                vs)))
        dict.update(self, other)

class BaseDependency(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.__class__.__name__ + " " + self.name
    def __repr__(self):
        return str(self)
    def install(self, osInterface, fake):
        osInterface.package_install(self.name, fake)
    def is_base(self):return True
    def distrib_name(self):
        return self.name

class EggDependency(BaseDependency):
    def __init__(self, name):
        BaseDependency.__init__(self, name)
    def install(self, osInterface, fake):
        raise NotImplementedError
    def is_base(self):return False
    def distrib_name(self):
        return ""

class InstallerDependency(BaseDependency):
    def __init__(self, name, path):
        BaseDependency.__init__(self, name)
        self.path = path
    def __str__(self):
        return BaseDependency.__str__(self) + ":" + self.path
    def install(self, osInterface, fake):
        raise NotImplementedError
    def is_base(self):return False
    def distrib_name(self):
        return ""





class Dependency(object):
    def __init__(self, package, _platform=False):
        self.__canonical_deps = []
        self.__distribution_deps = []
        self.__translation = {}
        self.__solve_dependencies(package, _platform)

    def __str__(self):
        return "canonical->%s\ndistribution->%s\ncompensated->%s"%(str(self.__canonical_deps),
                                                                 str(self.__translation.values()),
                                                                 str(self.other_packages()))

    def packages(self):
        return self.__canonical_deps

    def runtime_distribution_packages(self):
        return [dep for canoDep, dep in self.__translation.iteritems() if canoDep[-4:] != "-dev"]

    def development_distribution_packages(self):
        return [dep for canoDep, dep in self.__translation.iteritems() if canoDep[-4:] == "-dev"]

    def other_packages(self):
        return [dep for canoDep, dep in self.__translation.iteritems() if not dep.is_base()]

    ############################################################
    # Dependency solving and distribution translation follows: #
    ############################################################
    def __solve_dependencies(self, package, _platform=False):
        assert _platform is not None
        package_deps = dependencies.get_canonincal_dependencies().get(package, None)
        if not package_deps:
            raise Exception("No such package : " + package)

        if _platform == False:
            warnings.warn("No dependency de-canonification")

        # non recursive dependency browsing, Euler tour.
        pkgList = set()
        ancestors = collections.deque()
        childs = collections.deque()
        currentPkg = package
        currentPkgChilds = package_deps.__iter__()
        while currentPkg:
            hasChilds = True
            child = None
            try: child = currentPkgChilds.next()
            except: hasChilds = False
            if hasChilds:
                ancestors.append(currentPkg)
                childs.append(currentPkgChilds)
                currentPkg = child
                currentPkgChildsList = dependencies.get_canonincal_dependencies().get(currentPkg, None)
                if currentPkgChildsList:
                    currentPkgChilds = currentPkgChildsList.__iter__()
                else:
                    currentPkgChilds = None
            else:
                if currentPkg != package:
                    pkgList.add(currentPkg)
                    if len(ancestors) >= 1:
                        currentPkg = ancestors.pop()
                        currentPkgChilds = childs.pop()
                    else:
                        currentPkg = None #stops the loop
                else:
                    currentPkg = None

        pkgList = list(pkgList)
        self.__canonical_deps = pkgList

        #de-canonification
        if _platform:
            distribCls = DistributionPackageFactory().create(_platform)
            if distribCls:
                for pkg in self.__canonical_deps:
                    self.__translation[pkg] = distribCls[pkg]
        else:
            print "No decanonification"






# -- shortcuts for Openalea, VPlants and Alinea --
def Openalea(_platform=False):
    return Dependency("openalea", _platform)

def VPlants(_platform=False):
    return Dependency("vplants", _platform)

def Alinea(_platform=False):
    return Dependency("alinea", _platform)

