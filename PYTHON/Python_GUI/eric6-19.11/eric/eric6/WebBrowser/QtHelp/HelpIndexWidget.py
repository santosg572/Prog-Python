# -*- coding: utf-8 -*-

# Copyright (c) 2009 - 2019 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a window for showing the QtHelp index.
"""


from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QUrl, QEvent
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QMenu, QDialog, QApplication
)


class HelpIndexWidget(QWidget):
    """
    Class implementing a window for showing the QtHelp index.
    
    @signal escapePressed() emitted when the ESC key was pressed
    @signal openUrl(QUrl, str) emitted to open an entry in the current tab
    @signal newTab(QUrl, str) emitted to open an entry in a new tab
    @signal newBackgroundTab(QUrl, str) emitted to open an entry in a
        new background tab
    @signal newWindow(QUrl, str) emitted to open an entry in a new window
    """
    escapePressed = pyqtSignal()
    openUrl = pyqtSignal(QUrl)
    newTab = pyqtSignal(QUrl)
    newBackgroundTab = pyqtSignal(QUrl)
    newWindow = pyqtSignal(QUrl)
    
    def __init__(self, engine, parent=None):
        """
        Constructor
        
        @param engine reference to the help engine (QHelpEngine)
        @param parent reference to the parent widget (QWidget)
        """
        super(HelpIndexWidget, self).__init__(parent)
        
        self.__engine = engine
        
        self.__searchEdit = None
        self.__index = None
        
        self.__layout = QVBoxLayout(self)
        label = QLabel(self.tr("&Look for:"))
        self.__layout.addWidget(label)
        
        self.__searchEdit = QLineEdit()
        label.setBuddy(self.__searchEdit)
        self.__searchEdit.textChanged.connect(self.__filterIndices)
        self.__searchEdit.installEventFilter(self)
        self.__layout.addWidget(self.__searchEdit)
        
        self.__index = self.__engine.indexWidget()
        self.__index.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.__engine.indexModel().indexCreationStarted.connect(
            self.__disableSearchEdit)
        self.__engine.indexModel().indexCreated.connect(
            self.__enableSearchEdit)
        self.__index.linkActivated.connect(self.__linkActivated)
        self.__index.linksActivated.connect(self.__linksActivated)
        self.__index.customContextMenuRequested.connect(
            self.__showContextMenu)
        self.__searchEdit.returnPressed.connect(
            self.__index.activateCurrentItem)
        self.__layout.addWidget(self.__index)
    
    @pyqtSlot(QUrl, str)
    def __linkActivated(self, url, keyword, modifiers=None):
        """
        Private slot to handle the activation of a keyword entry.
        
        @param url URL of the selected entry
        @type QUrl
        @param keyword keyword for the URL
        @type str
        @keyparam modifiers keyboard modifiers
        @type Qt.KeyboardModifiers or None
        """
        if modifiers is None:
            modifiers = QApplication.keyboardModifiers()
        if not url.isEmpty() and url.isValid():
            if (
                modifiers & (Qt.ControlModifier | Qt.ShiftModifier) ==
                    (Qt.ControlModifier | Qt.ShiftModifier)
            ):
                self.newBackgroundTab.emit(url)
            elif modifiers & Qt.ControlModifier:
                self.newTab.emit(url)
            elif modifiers & Qt.ShiftModifier:
                self.newWindow.emit(url)
            else:
                self.openUrl.emit(url)
    
    def __linksActivated(self, links, keyword):
        """
        Private slot to handle the activation of an entry with multiple links.
        
        @param links dictionary containing the links
        @type dict of key:str and value:QUrl
        @param keyword keyword for the entry
        @type str
        """
        modifiers = QApplication.keyboardModifiers()
        if len(links) == 1:
            url = QUrl(links[list(links.keys())[0]])
        else:
            url = self.__selectLink(links, keyword)
        self.__linkActivated(url, keyword, modifiers)
    
    def __selectLink(self, links, keyword):
        """
        Private method to give the user a chance to select among the
        returned links.
        
        @param links dictionary of document title and URL to select from
        @type dictionary of str (key) and QUrl (value)
        @param keyword keyword for the link set
        @type str
        @return selected link
        @rtype QUrl
        """
        link = QUrl()
        from .HelpTopicDialog import HelpTopicDialog
        dlg = HelpTopicDialog(self, keyword, links)
        if dlg.exec_() == QDialog.Accepted:
            link = dlg.link()
        return link
    
    def __filterIndices(self, indexFilter):
        """
        Private slot to filter the indexes according to the given filter.
        
        @param indexFilter filter to be used (string)
        """
        if '*' in indexFilter:
            self.__index.filterIndices(indexFilter, indexFilter)
        else:
            self.__index.filterIndices(indexFilter)
    
    def __enableSearchEdit(self):
        """
        Private slot to enable the search edit.
        """
        self.__searchEdit.setEnabled(True)
        self.__filterIndices(self.__searchEdit.text())
    
    def __disableSearchEdit(self):
        """
        Private slot to enable the search edit.
        """
        self.__searchEdit.setEnabled(False)
    
    def focusInEvent(self, evt):
        """
        Protected method handling focus in events.
        
        @param evt reference to the focus event object (QFocusEvent)
        """
        if evt.reason() != Qt.MouseFocusReason:
            self.__searchEdit.selectAll()
            self.__searchEdit.setFocus()
    
    def eventFilter(self, watched, event):
        """
        Public method called to filter the event queue.
        
        @param watched the QObject being watched (QObject)
        @param event the event that occurred (QEvent)
        @return flag indicating whether the event was handled (boolean)
        """
        if (
            self.__searchEdit and watched == self.__searchEdit and
            event.type() == QEvent.KeyPress
        ):
            idx = self.__index.currentIndex()
            if event.key() == Qt.Key_Up:
                idx = self.__index.model().index(
                    idx.row() - 1, idx.column(), idx.parent())
                if idx.isValid():
                    self.__index.setCurrentIndex(idx)
            elif event.key() == Qt.Key_Down:
                idx = self.__index.model().index(
                    idx.row() + 1, idx.column(), idx.parent())
                if idx.isValid():
                    self.__index.setCurrentIndex(idx)
            elif event.key() == Qt.Key_Escape:
                self.escapePressed.emit()
        
        return QWidget.eventFilter(self, watched, event)
    
    def __showContextMenu(self, pos):
        """
        Private slot showing the context menu.
        
        @param pos position to show the menu at (QPoint)
        """
        idx = self.__index.indexAt(pos)
        if idx.isValid():
            menu = QMenu()
            curTab = menu.addAction(self.tr("Open Link"))
            newTab = menu.addAction(self.tr("Open Link in New Tab"))
            newBackgroundTab = menu.addAction(
                self.tr("Open Link in Background Tab"))
            newWindow = menu.addAction(self.tr("Open Link in New Window"))
            menu.move(self.__index.mapToGlobal(pos))
            
            act = menu.exec_()
            model = self.__index.model()
            if model is not None:
                keyword = model.data(idx, Qt.DisplayRole)
                links = model.linksForKeyword(keyword)
                if len(links) == 1:
                    link = QUrl(links[list(links.keys())[0]])
                else:
                    link = self.__selectLink(links, keyword)
                
                if not link.isEmpty() and link.isValid():
                    if act == curTab:
                        self.openUrl.emit(link)
                    elif act == newTab:
                        self.newTab.emit(link)
                    elif act == newBackgroundTab:
                        self.newBackgroundTab.emit(link)
                    elif act == newWindow:
                        self.newWindow.emit(link)
