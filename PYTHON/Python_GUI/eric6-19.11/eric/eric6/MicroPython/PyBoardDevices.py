# -*- coding: utf-8 -*-

# Copyright (c) 2019 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the device interface class for PyBoard boards.
"""

from E5Gui import E5MessageBox
from E5Gui.E5Application import e5App

from .MicroPythonDevices import MicroPythonDevice
from .MicroPythonWidget import HAS_QTCHART

import Utilities
import Preferences


class PyBoardDevice(MicroPythonDevice):
    """
    Class implementing the device for PyBoard boards.
    """
    DeviceVolumeName = "PYBFLASH"
    
    FlashInstructionsURL = (
        "https://github.com/micropython/micropython/wiki/"
        "Pyboard-Firmware-Update"
    )
    
    def __init__(self, microPythonWidget, parent=None):
        """
        Constructor
        
        @param microPythonWidget reference to the main MicroPython widget
        @type MicroPythonWidget
        @param parent reference to the parent object
        @type QObject
        """
        super(PyBoardDevice, self).__init__(microPythonWidget, parent)
    
    def setButtons(self):
        """
        Public method to enable the supported action buttons.
        """
        super(PyBoardDevice, self).setButtons()
        self.microPython.setActionButtons(
            run=True, repl=True, files=True, chart=HAS_QTCHART)
        
        if self.__deviceVolumeMounted():
            self.microPython.setActionButtons(open=True, save=True)
    
    def forceInterrupt(self):
        """
        Public method to determine the need for an interrupt when opening the
        serial connection.
        
        @return flag indicating an interrupt is needed
        @rtype bool
        """
        return False
    
    def deviceName(self):
        """
        Public method to get the name of the device.
        
        @return name of the device
        @rtype str
        """
        return self.tr("PyBoard")
    
    def canStartRepl(self):
        """
        Public method to determine, if a REPL can be started.
        
        @return tuple containing a flag indicating it is safe to start a REPL
            and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return True, ""
    
    def canStartPlotter(self):
        """
        Public method to determine, if a Plotter can be started.
        
        @return tuple containing a flag indicating it is safe to start a
            Plotter and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return True, ""
    
    def canRunScript(self):
        """
        Public method to determine, if a script can be executed.
        
        @return tuple containing a flag indicating it is safe to start a
            Plotter and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return True, ""
    
    def runScript(self, script):
        """
        Public method to run the given Python script.
        
        @param script script to be executed
        @type str
        """
        pythonScript = script.split("\n")
        self.sendCommands(pythonScript)
    
    def canStartFileManager(self):
        """
        Public method to determine, if a File Manager can be started.
        
        @return tuple containing a flag indicating it is safe to start a
            File Manager and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return True, ""
    
    def supportsLocalFileAccess(self):
        """
        Public method to indicate file access via a local directory.
        
        @return flag indicating file access via local directory
        @rtype bool
        """
        return self.__deviceVolumeMounted()
    
    def __deviceVolumeMounted(self):
        """
        Private method to check, if the device volume is mounted.
        
        @return flag indicated a mounted device
        @rtype bool
        """
        return self.getWorkspace(silent=True).endswith(self.DeviceVolumeName)
    
    def getWorkspace(self, silent=False):
        """
        Public method to get the workspace directory.
        
        @param silent flag indicating silent operations
        @type bool
        @return workspace directory used for saving files
        @rtype str
        """
        # Attempts to find the path on the filesystem that represents the
        # plugged in PyBoard board.
        deviceDirectory = Utilities.findVolume(self.DeviceVolumeName)
        
        if deviceDirectory:
            return deviceDirectory
        else:
            # return the default workspace and give the user a warning (unless
            # silent mode is selected)
            if not silent:
                E5MessageBox.warning(
                    self.microPython,
                    self.tr("Workspace Directory"),
                    self.tr("Python files for PyBoard devices are stored"
                            " on the device. Therefore, to edit these files"
                            " you need to have the device plugged in. Until"
                            " you plug in a device, the standard directory"
                            " will be used."))
            
            return super(PyBoardDevice, self).getWorkspace()
    
    def getDocumentationUrl(self):
        """
        Public method to get the device documentation URL.
        
        @return documentation URL of the device
        @rtype str
        """
        return Preferences.getMicroPython("MicroPythonDocuUrl")
    
    def addDeviceMenuEntries(self, menu):
        """
        Public method to add device specific entries to the given menu.
        
        @param menu reference to the context menu
        @type QMenu
        """
        menu.addAction(
            self.tr("MicroPython Install Instructions"),
            self.__showInstallInstructions)
        # TODO: add entry to flash a new firmware using dfu-util
    
    def __showInstallInstructions(self):
        """
        Private slot to open the URL containing instructions for installing
        MicroPython on the pyboard.
        """
        e5App().getObject("UserInterface").launchHelpViewer(
            PyBoardDevice.FlashInstructionsURL)
