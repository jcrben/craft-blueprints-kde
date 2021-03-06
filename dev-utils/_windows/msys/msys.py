import io

import info
import shells

from CraftOS.osutils import OsUtils

from Package.MaybeVirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "20181211"
        # don't set an actual version  instead of base. Msys must be manually updated so doing a craft update of msys wil break things.
        self.targets["base"] = f"http://repo.msys2.org/distrib/x86_64/msys2-base-x86_64-{ver}.tar.xz"
        self.targetInstSrc["base"] = "msys64"
        self.targetInstallPath["base"] = "msys"
        self.targetDigests["base"] = (['5cab863861bc9d414b4df2cbe0b1bf8b560eb9a19aa637afabd6f436b572f2e3'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "base"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None
        self.runtimeDependencies["dev-utils/python3"] = None

    def msysInstallShim(self, installDir):
        return utils.createShim(os.path.join(installDir, "dev-utils", "bin", "msys.exe"),
                                os.path.join(installDir, "dev-utils", "bin", "python3.exe"),
                                args=os.path.join(CraftStandardDirs.craftBin(), "shells.py"))


from Package.BinaryPackageBase import *


class MsysPackage(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.shell = shells.BashShell()

    def postInstall(self):
        return self.subinfo.msysInstallShim(self.imageDir())

    def postQmerge(self):
        msysDir = os.path.join(CraftStandardDirs.craftRoot(), "msys")

        def stopProcesses():
            return OsUtils.killProcess("*", msysDir)

        def queryForUpdate():
            out = io.BytesIO()
            if not self.shell.execute(".", "pacman", "-Sy --noconfirm --force"):
                raise Exception()
            self.shell.execute(".", "pacman", "-Qu --noconfirm", stdout=out, stderr=subprocess.PIPE)
            out = out.getvalue()
            return out != b""

        # start and restart msys before first use
        if not (self.shell.execute(".", "echo", "Firstrun") and
                stopProcesses() and
                self.shell.execute(".", "pacman-key", "--init") and
                self.shell.execute(".", "pacman-key", "--populate")):
            return False

        try:
            while queryForUpdate():
                if not (self.shell.execute(".", "pacman", "-Su --noconfirm --force --ask 20") and
                        stopProcesses()):
                    return False
        except Exception as e:
            print(e)
            return False
        if not (self.shell.execute(".", "pacman", "-S base-devel msys/binutils --noconfirm --force --needed") and
                stopProcesses()):
            return False
        return utils.system("autorebase.bat", cwd=msysDir)


class VirtualPackage(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)

    def install(self):
        if not VirtualPackageBase.install(self):
            return False
        return self.subinfo.msysInstallShim(self.imageDir())


class Package(MaybeVirtualPackageBase):
    def __init__(self):
        self.skipCondition = ("Paths", "Msys") not in CraftCore.settings
        MaybeVirtualPackageBase.__init__(self, condition=self.skipCondition, classA=MsysPackage, classB=VirtualPackage)

        if not self.skipCondition:
            # override the install method
            def install():
                CraftCore.log.info(f"Using manually installed msys {CraftStandardDirs.msysDir()}")
                return self.baseClass.install(self)

            setattr(self, "install", install)
