#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2019 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Eric6 Web Browser.

This is the main Python script that performs the necessary initialization
of the web browser and starts the Qt event loop. This is a standalone version
of the integrated web browser. It is based on QtWebEngine.
"""


import sys
import os

sys.path.insert(1, os.path.dirname(__file__))

try:
    try:
        from PyQt5 import sip       # __IGNORE_EXCEPTION__
    except ImportError:
        import sip
    sip.setdestroyonexit(False)
except AttributeError:
    pass

app = None
SettingsDir = None

for arg in sys.argv[:]:
    if arg.startswith("--config="):
        import Globals
        configDir = arg.replace("--config=", "")
        Globals.setConfigDir(configDir)
        sys.argv.remove(arg)
    elif arg.startswith("--settings="):
        from PyQt5.QtCore import QSettings
        SettingsDir = os.path.expanduser(arg.replace("--settings=", ""))
        if not os.path.isdir(SettingsDir):
            os.makedirs(SettingsDir)
        QSettings.setPath(QSettings.IniFormat, QSettings.UserScope,
                          SettingsDir)
        sys.argv.remove(arg)

# make ThirdParty package available as a packages repository
sys.path.insert(2, os.path.join(os.path.dirname(__file__),
                                "ThirdParty", "Pygments"))
sys.path.insert(2, os.path.join(os.path.dirname(__file__),
                                "ThirdParty", "EditorConfig"))

try:
    from PyQt5 import QtWebEngineWidgets    # __IGNORE_WARNING__
except ImportError:
    if "--quiet" not in sys.argv:
        from PyQt5.QtCore import QTimer
        from PyQt5.QtWidgets import QApplication
        from E5Gui import E5MessageBox          # __IGNORE_WARNING__
        app = QApplication([])
        QTimer.singleShot(0, lambda: E5MessageBox.critical(
            None,
            "eric6 Web Browser",
            "QtWebEngineWidgets is not installed but needed to execute the"
            " web browser."))
        app.exec_()
    sys.exit(100)

import Globals
from Globals import AppInfo, qVersionTuple

from E5Gui.E5Application import E5Application

from Toolbox import Startup

from WebBrowser.WebBrowserSingleApplication import (
    WebBrowserSingleApplicationClient
)


def createMainWidget(argv):
    """
    Function to create the main widget.
    
    @param argv list of command line parameters
    @type list of str
    @return reference to the main widget
    @rtype QWidget
    """
    from WebBrowser.WebBrowserWindow import WebBrowserWindow
    
    searchWord = None
    private = False
    qthelp = False
    single = False
    name = ""
    
    for arg in reversed(argv):
        if arg.startswith("--search="):
            searchWord = argv[1].split("=", 1)[1]
            argv.remove(arg)
        elif arg.startswith("--name="):
            name = arg.replace("--name=", "")
            argv.remove(arg)
        elif arg.startswith("--newtab="):
            # only used for single application client
            argv.remove(arg)
        elif arg == "--private":
            private = True
            argv.remove(arg)
        elif arg == "--qthelp":
            qthelp = True
            argv.remove(arg)
        elif arg == "--quiet":
            # only needed until we reach this point
            argv.remove(arg)
        elif arg == "--single":
            single = True
            argv.remove(arg)
        elif arg.startswith("--"):
            argv.remove(arg)
    
    try:
        home = argv[1]
    except IndexError:
        home = ""
    
    browser = WebBrowserWindow(home, '.', None, 'web_browser',
                               searchWord=searchWord, private=private,
                               settingsDir=SettingsDir, qthelp=qthelp,
                               single=single, saname=name)
    return browser


def main():
    """
    Main entry point into the application.
    """
    global app
    
    options = [
        ("--config=configDir",
         "use the given directory as the one containing the config files"),
        ("--private", "start the browser in private browsing mode"),
        ("--qthelp", "start the browser with support for QtHelp"),
        ("--quiet", "don't show any startup error messages"),
        ("--search=word", "search for the given word"),
        ("--settings=settingsDir",
         "use the given directory to store the settings files"),
        ("--single", "start the browser as a single application"),
    ]
    appinfo = AppInfo.makeAppInfo(sys.argv,
                                  "eric6 Web Browser",
                                  "file",
                                  "web browser",
                                  options)
    
    # set the library paths for plugins
    Startup.setLibraryPaths()
    
    if qVersionTuple() >= (5, 12, 0):
        from PyQt5.QtWebEngineCore import QWebEngineUrlScheme
        scheme = QWebEngineUrlScheme(b"eric")
        scheme.setSyntax(QWebEngineUrlScheme.Syntax.Path)
        scheme.setFlags(QWebEngineUrlScheme.SecureScheme |
                        QWebEngineUrlScheme.ContentSecurityPolicyIgnored)
        QWebEngineUrlScheme.registerScheme(scheme)
    if "--qthelp" in sys.argv and qVersionTuple() >= (5, 12, 0):
        from PyQt5.QtWebEngineCore import QWebEngineUrlScheme
        scheme = QWebEngineUrlScheme(b"qthelp")
        scheme.setSyntax(QWebEngineUrlScheme.Syntax.Path)
        scheme.setFlags(QWebEngineUrlScheme.SecureScheme)
        QWebEngineUrlScheme.registerScheme(scheme)
    
    app = E5Application(sys.argv)
    if "--private" not in sys.argv:
        client = WebBrowserSingleApplicationClient()
        res = client.connect()
        if res > 0:
            if len(sys.argv) > 1:
                client.processArgs(sys.argv[1:])
            sys.exit(0)
        elif res < 0:
            print("eric6_browser: {0}".format(client.errstr()))
            # __IGNORE_WARNING_M801__
            sys.exit(res)
    
    res = Startup.simpleAppStartup(sys.argv,
                                   appinfo,
                                   createMainWidget,
                                   installErrorHandler=True,
                                   app=app)
    sys.exit(res)

if __name__ == '__main__':
    main()
