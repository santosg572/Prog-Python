#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2007 - 2019 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Eric6 Plugin Installer.

This is the main Python script to install eric6 plugins from outside of the
IDE.
"""


import sys
import os

sys.path.insert(1, os.path.dirname(__file__))

for arg in sys.argv[:]:
    if arg.startswith("--config="):
        import Globals
        configDir = arg.replace("--config=", "")
        Globals.setConfigDir(configDir)
        sys.argv.remove(arg)
    elif arg.startswith("--settings="):
        from PyQt5.QtCore import QSettings
        settingsDir = os.path.expanduser(arg.replace("--settings=", ""))
        if not os.path.isdir(settingsDir):
            os.makedirs(settingsDir)
        QSettings.setPath(QSettings.IniFormat, QSettings.UserScope,
                          settingsDir)
        sys.argv.remove(arg)

from Globals import AppInfo

from Toolbox import Startup


def createMainWidget(argv):
    """
    Function to create the main widget.
    
    @param argv list of commandline parameters (list of strings)
    @return reference to the main widget (QWidget)
    """
    from PluginManager.PluginRepositoryDialog import PluginRepositoryWindow
    return PluginRepositoryWindow(None)


def main():
    """
    Main entry point into the application.
    """
    options = [
        ("--config=configDir",
         "use the given directory as the one containing the config files"),
        ("--settings=settingsDir",
         "use the given directory to store the settings files"),
    ]
    appinfo = AppInfo.makeAppInfo(sys.argv,
                                  "Eric6 Plugin Repository",
                                  "",
                                  "Utility to show the contents of the eric6"
                                  " Plugin repository.",
                                  options)
    res = Startup.simpleAppStartup(sys.argv,
                                   appinfo,
                                   createMainWidget)
    sys.exit(res)

if __name__ == '__main__':
    main()
