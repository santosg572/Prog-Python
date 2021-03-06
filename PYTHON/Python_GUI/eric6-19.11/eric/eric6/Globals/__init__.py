# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2019 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module defining common data to be used by all modules.
"""

#
# Note: Do not import any eric stuff in here!!!!!!!
#


import sys
import os
import re
import shutil

from PyQt5.QtCore import (
    QDir, QLibraryInfo, QByteArray, QCoreApplication, QT_VERSION_STR,
    QT_VERSION, QProcess, qVersion
)

# names of the various settings objects
settingsNameOrganization = "Eric6"
settingsNameGlobal = "eric6"
settingsNameRecent = "eric6recent"

# key names of the various recent entries
recentNameMultiProject = "MultiProjects"
recentNameProject = "Projects"
recentNameFiles = "Files"
recentNameHexFiles = "HexFiles"
recentNameHosts = "Hosts6"
recentNameBreakpointFiles = "BreakPointFiles"
recentNameBreakpointConditions = "BreakPointConditions"

configDir = None


def isWindowsPlatform():
    """
    Function to check, if this is a Windows platform.
    
    @return flag indicating Windows platform (boolean)
    """
    return sys.platform.startswith(("win", "cygwin"))


def isMacPlatform():
    """
    Function to check, if this is a Mac platform.
    
    @return flag indicating Mac platform (boolean)
    """
    return sys.platform == "darwin"


def isLinuxPlatform():
    """
    Function to check, if this is a Linux platform.
    
    @return flag indicating Linux platform (boolean)
    """
    return sys.platform.startswith("linux")


def desktopName():
    """
    Function to determine the name of the desktop environment used
    (Linux only).
    
    @return name of the desktop environment
    @rtype str
    """
    if not isLinuxPlatform():
        return ""
    
    currDesktop = os.environ.get("XDG_CURRENT_DESKTOP", "")
    if currDesktop:
        return currDesktop
    
    currDesktop = os.environ.get("XDG_SESSION_DESKTOP", "")
    if currDesktop:
        return currDesktop
    
    currDesktop = os.environ.get("GDMSESSION", "")
    if currDesktop:
        return currDesktop
    
    currDesktop = os.environ.get("GNOME_DESKTOP_SESSION_ID", "")
    if currDesktop:
        return currDesktop
    
    currDesktop = os.environ.get("KDE_FULL_SESSION", "")
    if currDesktop:
        return currDesktop
    
    currDesktop = os.environ.get("DESKTOP_SESSION", "")
    if currDesktop:
        return currDesktop
    
    return ""


def isKdeDesktop():
    """
    Function to check, if the current session is a KDE desktop (Linux only).
    
    @return flag indicating a KDE desktop
    @rtype bool
    """
    if not isLinuxPlatform():
        return False
    
    isKDE = False
    
    desktop = (
        os.environ.get("XDG_CURRENT_DESKTOP", "").lower() or
        os.environ.get("XDG_SESSION_DESKTOP", "").lower() or
        os.environ.get("DESKTOP_SESSION", "").lower()
    )
    if desktop:
        isKDE = "kde" in desktop or "plasma" in desktop
    else:
        isKDE = bool(os.environ.get("KDE_FULL_SESSION", ""))
    
    return isKDE


def isGnomeDesktop():
    """
    Function to check, if the current session is a Gnome desktop (Linux only).
    
    @return flag indicating a Gnome desktop
    @rtype bool
    """
    if not isLinuxPlatform():
        return False
    
    isGnome = False
    
    desktop = (
        os.environ.get("XDG_CURRENT_DESKTOP", "").lower() or
        os.environ.get("XDG_SESSION_DESKTOP", "").lower() or
        os.environ.get("GDMSESSION", "").lower()
    )
    if desktop:
        isGnome = "gnome" in desktop
    else:
        isGnome = bool(os.environ.get("GNOME_DESKTOP_SESSION_ID", ""))
    
    return isGnome


def sessionType():
    """
    Function to determine the name of the running session (Linux only).
    
    @return name of the desktop environment
    @rtype str
    """
    if not isLinuxPlatform():
        return ""
    
    sessionType = os.environ.get("XDG_SESSION_TYPE").lower()
    if "x11" in sessionType:
        return "X11"
    elif "wayland" in sessionType:
        return "Wayland"
    
    sessionType = os.environ.get("WAYLAND_DISPLAY", "").lower()
    if "wayland" in sessionType:
        return "Wayland"
    
    return ""


def isWaylandSession():
    """
    Function to check, if the current session is a wayland session.
    
    @return flag indicating a wayland session
    @rtype bool
    """
    return sessionType() == "Wayland"


def getConfigDir():
    """
    Module function to get the name of the directory storing the config data.
    
    @return directory name of the config dir (string)
    """
    if configDir is not None and os.path.exists(configDir):
        hp = configDir
    else:
        cdn = ".eric6"
        if isWindowsPlatform():
            # migrate the old config directory (< v18.06)
            cdnOld = "_eric6"
            hpOld = os.path.join(os.path.expanduser("~"), cdnOld)
            if os.path.exists(hpOld):
                hpNew = os.path.join(os.path.expanduser("~"), cdn)
                if os.path.exists(hpNew):
                    # simply delete the old config directory
                    shutil.rmtree(hpOld, True)
                else:
                    os.rename(hpOld, hpNew)
        
        hp = os.path.join(os.path.expanduser("~"), cdn)
        if not os.path.exists(hp):
            os.mkdir(hp)
    return hp


def setConfigDir(d):
    """
    Module function to set the name of the directory storing the config data.
    
    @param d name of an existing directory (string)
    """
    global configDir
    configDir = os.path.expanduser(d)


def getPythonModulesDirectory():
    """
    Function to determine the path to Python's modules directory.
    
    @return path to the Python modules directory (string)
    """
    import distutils.sysconfig
    return distutils.sysconfig.get_python_lib(True)


def getPyQt5ModulesDirectory():
    """
    Function to determine the path to PyQt5 modules directory.
    
    @return path to the PyQt5 modules directory (string)
    """
    import distutils.sysconfig
    
    pyqtPath = os.path.join(distutils.sysconfig.get_python_lib(True), "PyQt5")
    if os.path.exists(pyqtPath):
        return pyqtPath
    
    return ""
    

def getPyQtToolsPath(version=5):
    """
    Module function to get the path of the PyQt tools.
    
    @param version PyQt major version
    @type int
    @return path to the PyQt tools
    @rtype str
    """
    import Preferences
    
    path = ""
    
    # step 1: check, if the user has configured a tools path
    path = Preferences.getQt("PyQtToolsDir")
    
    # step 2: determine from used Python interpreter (pyrcc is test object)
    if not path:
        program = "pyrcc{0}".format(version)
        if isWindowsPlatform():
            program += ".exe"
            dirName = os.path.dirname(sys.executable)
            if os.path.exists(os.path.join(dirName, program)):
                path = dirName
            elif os.path.exists(os.path.join(dirName, "Scripts", program)):
                path = os.path.join(dirName, "Scripts")
        else:
            dirName = os.path.dirname(sys.executable)
            if os.path.exists(os.path.join(dirName, program)):
                path = dirName
    
    return path


def getQtBinariesPath():
    """
    Module function to get the path of the Qt binaries.
    
    @return path of the Qt binaries (string)
    """
    import Preferences
    
    path = ""
    
    # step 1: check, if the user has configured a tools path
    path = Preferences.getQt("QtToolsDir")
    
    if not path and isWindowsPlatform():
        # step 2.1: check for PyQt5 Windows installer (designer is test object)
        modDir = getPyQt5ModulesDirectory()
        if os.path.exists(os.path.join(modDir, "bin", "designer.exe")):
            path = os.path.join(modDir, "bin")
        elif os.path.exists(os.path.join(modDir, "designer.exe")):
            path = modDir
        
        if not path:
            import distutils.sysconfig
            # step 2.2.1: check for the pyqt5-tools wheel (new variant)
            # (Windows only)
            pyqt5ToolsPath = os.path.join(
                distutils.sysconfig.get_python_lib(True), "pyqt5_tools")
            if os.path.exists(os.path.join(pyqt5ToolsPath, "designer.exe")):
                path = pyqt5ToolsPath
            if not path:
                # step 2.2.2: check for the pyqt5-tools wheel (old variant)
                # (Windows only)
                pyqt5ToolsPath = os.path.join(
                    distutils.sysconfig.get_python_lib(True), "pyqt5-tools")
                if os.path.exists(os.path.join(pyqt5ToolsPath,
                                               "designer.exe")):
                    path = pyqt5ToolsPath
    
    if not path:
        # step 3: get the path from Qt
        # Note: no Qt tools are to be found there for PyQt 5.7.0
        path = QLibraryInfo.location(QLibraryInfo.BinariesPath)
        if not os.path.exists(path):
            path = ""
    
    return QDir.toNativeSeparators(path)


def translate(*args):
    """
    Module function to handle different PyQt 4/5 QCoreApplication.translate
    parameter.
    
    @param args tuple of arguments from QCoreApplication.translate (tuple)
    @return translated string (string)
    """
    if QT_VERSION_STR.startswith('4.'):
        args = list(args)
        args.insert(3, QCoreApplication.CodecForTr)
    return QCoreApplication.translate(*args)


###############################################################################
## functions for version handling
###############################################################################


def versionToTuple(version):
    """
    Module function to convert a version string into a tuple.
    
    Note: A version string consists of non-negative decimals separated by "."
    optionally followed by a suffix. Suffix is everything after the last
    decimal.
    
    @param version version string
    @type str
    @return version tuple without the suffix
    @rtype tuple of int
    """
    versionParts = []
    
    # step 1: extract suffix
    version = re.split(r"[^\d.]", version)[0]
    for part in version.split("."):
        versionParts.append(int(part))
    
    return tuple(versionParts)


def qVersionTuple():
    """
    Module function to get the Qt version as a tuple.
    
    @return Qt version as a tuple
    @rtype tuple of int
    """
    return (
        (QT_VERSION & 0xff0000) >> 16,
        (QT_VERSION & 0xff00) >> 8,
        QT_VERSION & 0xff,
    )


###############################################################################
## functions for extended string handling
###############################################################################


def strGroup(txt, sep, groupLen=4):
    """
    Module function to group a string into sub-strings separated by a
    separator.
    
    @param txt text to be grouped
    @type str
    @param sep separator string
    @type str
    @param groupLen length of each group
    @type int
    @return result string
    @rtype str
    """
    groups = []
    
    while len(txt) // groupLen != 0:
        groups.insert(0, txt[-groupLen:])
        txt = txt[:-groupLen]
    if len(txt) > 0:
        groups.insert(0, txt)
    return sep.join(groups)


def strToQByteArray(txt):
    """
    Module function to convert a Python string into a QByteArray.
    
    @param txt Python string to be converted
    @type str, bytes, bytearray, unicode
    @return converted QByteArray
    @rtype QByteArray
    """
    if isinstance(txt, str):
        txt = txt.encode("utf-8")
    
    return QByteArray(txt)


def dataString(size):
    """
    Module function to generate a formatted size string.
    
    @param size size to be formatted
    @type int
    @return formatted data string
    @rtype str
    """
    if size < 1024:
        return QCoreApplication.translate(
            "Globals", "{0:4.2f} Bytes").format(size)
    elif size < 1024 * 1024:
        size /= 1024
        return QCoreApplication.translate(
            "Globals", "{0:4.2f} KiB").format(size)
    elif size < 1024 * 1024 * 1024:
        size /= 1024 * 1024
        return QCoreApplication.translate(
            "Globals", "{0:4.2f} MiB").format(size)
    elif size < 1024 * 1024 * 1024 * 1024:
        size /= 1024 * 1024 * 1024
        return QCoreApplication.translate(
            "Globals", "{0:4.2f} GiB").format(size)
    else:
        size /= 1024 * 1024 * 1024 * 1024
        return QCoreApplication.translate(
            "Globals", "{0:4.2f} TiB").format(size)


###############################################################################
## functions for converting QSetting return types to valid types
###############################################################################


def toBool(value):
    """
    Module function to convert a value to bool.
    
    @param value value to be converted
    @return converted data
    """
    if value in ["true", "1", "True"]:
        return True
    elif value in ["false", "0", "False"]:
        return False
    else:
        return bool(value)


def toList(value):
    """
    Module function to convert a value to a list.
    
    @param value value to be converted
    @return converted data
    """
    if value is None:
        return []
    elif not isinstance(value, list):
        return [value]
    else:
        return value


def toByteArray(value):
    """
    Module function to convert a value to a byte array.
    
    @param value value to be converted
    @return converted data
    """
    if value is None:
        return QByteArray()
    else:
        return value


def toDict(value):
    """
    Module function to convert a value to a dictionary.
    
    @param value value to be converted
    @return converted data
    """
    if value is None:
        return {}
    else:
        return value


###############################################################################
## functions for web browser variant detection
###############################################################################


def getWebBrowserSupport():
    """
    Module function to determine the supported web browser variant.
    
    @return string indicating the supported web browser variant ("QtWebEngine",
        or "None")
    @rtype str
    """
    from eric6config import getConfig
    scriptPath = os.path.join(getConfig("ericDir"), "Tools",
                              "webBrowserSupport.py")
    proc = QProcess()
    proc.start(sys.executable, [scriptPath, qVersion()])
    if proc.waitForFinished(10000):
        variant = str(proc.readAllStandardOutput(), "utf-8", 'replace').strip()
    else:
        variant = "None"
    return variant
#
# eflag: noqa = M801
