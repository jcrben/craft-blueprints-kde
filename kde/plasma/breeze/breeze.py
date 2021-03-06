import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.patchToApply["5.14.4"] = [("breeze-5.14.5-20190125.diff", 1)]
        self.patchToApply["5.14.5"] = [("breeze-5.14.5-20190125.diff", 1)]
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier4/frameworkintegration"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier3/plasma-framework"] = None
        self.runtimeDependencies["kde/plasma/kdecoration"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
