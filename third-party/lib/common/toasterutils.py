import sys, os, imp, glob


### Loads an import name
def loadImportName(importname):
	print(' importing :: ' + importname)
        moduleLoaded = None
        try:
                moduleLoaded =  sys.modules[importname]
        except KeyError:
                pass
        fp, pathname, description = imp.find_module(importname)

        try:
                moduleLoaded = imp.load_module(importname, fp, pathname, description)
        finally:
                # Since we may exit via an exception, close fp explicitly.
                if fp:
                        fp.close()
        return moduleLoaded
