# -*- coding: utf-8 -*-

# Copyright (c) 2019 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to select the heads to be closed.
"""


import os

from PyQt5.QtCore import pyqtSlot, QProcess
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QTreeWidgetItem

from .Ui_HgCloseHeadSelectionDialog import Ui_HgCloseHeadSelectionDialog


class HgCloseHeadSelectionDialog(QDialog, Ui_HgCloseHeadSelectionDialog):
    """
    Class implementing a dialog to select the heads to be closed.
    """
    def __init__(self, vcs, ppath, parent=None):
        """
        Constructor
        
        @param vcs reference to the VCS object
        @type Hg
        @param ppath directory containing the repository
        @type str
        @param parent reference to the parent widget
        @type QWidget
        """
        super(HgCloseHeadSelectionDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.buttonBox.button(QDialogButtonBox.Cancel).setDefault(True)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        
        heads = self.__getHeads(vcs, ppath)
        for revision, branch in heads:
            QTreeWidgetItem(self.headsList, [revision, branch])
    
    def __getHeads(self, vcs, ppath):
        """
        Private method to get the open heads.
        
        @param vcs reference to the VCS object
        @type Hg
        @param ppath directory containing the repository
        @type str
        @return list of tuples containing the revision and the corresponding
            branch name
        @rtype list of tuples of (str, str)
        """
        args = vcs.initCommand("heads")
        args.append('--template')
        args.append('{node|short}@@@{branches}\n')
        
        output = ""
        client = vcs.getClient()
        if client is None:
            # find the root of the repo
            repodir = self.splitPath(ppath)[0]
            while not os.path.isdir(os.path.join(repodir, self.adminDir)):
                repodir = os.path.dirname(repodir)
                if os.path.splitdrive(repodir)[1] == os.sep:
                    return []
            
            process = QProcess()
            process.setWorkingDirectory(repodir)
            process.start('hg', args)
            procStarted = process.waitForStarted(5000)
            if procStarted:
                finished = process.waitForFinished(30000)
                if finished and process.exitCode() == 0:
                    output = str(process.readAllStandardOutput(),
                                 self.getEncoding(), 'replace')
        else:
            output, error = client.runcommand(args)
        
        heads = []
        if output:
            for line in output.splitlines():
                line = line.strip()
                if line:
                    revision, branch = line.split("@@@")
                    heads.append((revision, branch))
            
        return heads
    
    @pyqtSlot()
    def on_headsList_itemSelectionChanged(self):
        """
        Private slot handling changes of the selection.
        """
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(
            len(self.headsList.selectedItems()) > 0
        )
    
    def getData(self):
        """
        Public method to retrieve the entered data.
        
        @return tuple containing a list of selected revisions and the commit
            message
        @rtype tuple of (list of str, str)
        """
        revisions = [itm.text(0) for itm in self.headsList.selectedItems()]
        message = self.logEdit.toPlainText().strip()
        
        return revisions, message
