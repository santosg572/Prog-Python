# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2019 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the AdBlock icon for the main window status bar.
"""


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QMenu

from E5Gui.E5ClickableLabel import E5ClickableLabel

import UI.PixmapCache


class AdBlockIcon(E5ClickableLabel):
    """
    Class implementing the AdBlock icon for the main window status bar.
    """
    def __init__(self, parent):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type WebBrowserWindow
        """
        super(AdBlockIcon, self).__init__(parent)
        
        self.__mw = parent
        self.__menuAction = None
        self.__enabled = False
        
        self.setMaximumHeight(16)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(self.tr(
            "AdBlock lets you block unwanted content on web pages."))
        
        self.clicked.connect(self.__showMenu)
    
    def setEnabled(self, enabled):
        """
        Public slot to set the enabled state.
        
        @param enabled enabled state
        @type bool
        """
        self.__enabled = enabled
        if enabled:
            self.currentChanged()
        else:
            self.setPixmap(
                UI.PixmapCache.getPixmap("adBlockPlusDisabled16.png"))
    
    def __createMenu(self, menu):
        """
        Private slot to create the context menu.
        
        @param menu parent menu
        @type QMenu
        """
        menu.clear()
        
        manager = self.__mw.adBlockManager()
        
        if manager.isEnabled():
            act = menu.addAction(
                UI.PixmapCache.getIcon("adBlockPlusDisabled.png"),
                self.tr("Disable AdBlock"))
            act.setData(False)
            act.triggered.connect(lambda: self.__enableAdBlock(act))
        else:
            act = menu.addAction(
                UI.PixmapCache.getIcon("adBlockPlus.png"),
                self.tr("Enable AdBlock"))
            act.setData(True)
            act.triggered.connect(lambda: self.__enableAdBlock(act))
        menu.addSeparator()
        if manager.isEnabled() and self.__mw.currentBrowser().url().host():
            if self.__isCurrentHostExcepted():
                act = menu.addAction(
                    UI.PixmapCache.getIcon("adBlockPlus.png"),
                    self.tr("Remove AdBlock Exception"))
                act.setData(False)
                act.triggered.connect(lambda: self.__setException(act))
            else:
                act = menu.addAction(
                    UI.PixmapCache.getIcon("adBlockPlusGreen.png"),
                    self.tr("Add AdBlock Exception"))
                act.setData(True)
                act.triggered.connect(lambda: self.__setException(act))
        menu.addAction(
            UI.PixmapCache.getIcon("adBlockPlusGreen.png"),
            self.tr("AdBlock Exceptions..."), manager.showExceptionsDialog)
        menu.addSeparator()
        menu.addAction(
            UI.PixmapCache.getIcon("adBlockPlus.png"),
            self.tr("AdBlock Configuration..."), manager.showDialog)
    
    def menuAction(self):
        """
        Public method to get a reference to the menu action.
        
        @return reference to the menu action
        @rtype QAction
        """
        if not self.__menuAction:
            self.__menuAction = QAction(self.tr("AdBlock"), self)
            self.__menuAction.setMenu(QMenu())
            self.__menuAction.menu().aboutToShow.connect(
                lambda: self.__createMenu(self.__menuAction.menu()))
        
        if self.__enabled:
            self.__menuAction.setIcon(
                UI.PixmapCache.getIcon("adBlockPlus.png"))
        else:
            self.__menuAction.setIcon(
                UI.PixmapCache.getIcon("adBlockPlusDisabled.png"))
        
        return self.__menuAction
    
    def __showMenu(self, pos):
        """
        Private slot to show the context menu.
        
        @param pos position the context menu should be shown
        @type QPoint
        """
        menu = QMenu()
        self.__createMenu(menu)
        menu.exec_(pos)
    
    def __enableAdBlock(self, act):
        """
        Private slot to enable or disable AdBlock.
        
        @param act reference to the action
        @type QAction
        """
        self.__mw.adBlockManager().setEnabled(act.data())
    
    def __isCurrentHostExcepted(self):
        """
        Private method to check, if the host of the current browser is
        excepted.
        
        @return flag indicating an exception
        @rtype bool
        """
        browser = self.__mw.currentBrowser()
        if browser is None:
            return False
        
        urlHost = browser.page().url().host()
        
        return (
            urlHost and
            self.__mw.adBlockManager().isHostExcepted(urlHost)
        )
    
    def currentChanged(self):
        """
        Public slot to handle a change of the current browser tab.
        """
        if self.__enabled:
            if self.__isCurrentHostExcepted():
                self.setPixmap(
                    UI.PixmapCache.getPixmap("adBlockPlusGreen16.png"))
            else:
                self.setPixmap(UI.PixmapCache.getPixmap("adBlockPlus16.png"))
    
    def __setException(self, act):
        """
        Private slot to add or remove the current host from the list of
        exceptions.
        
        @param act referenced to the action
        @type QAction
        """
        urlHost = self.__mw.currentBrowser().url().host()
        if act.data():
            self.__mw.adBlockManager().addException(urlHost)
        else:
            self.__mw.adBlockManager().removeException(urlHost)
        self.currentChanged()
    
    def sourceChanged(self, browser, url):
        """
        Public slot to handle URL changes.
        
        @param browser reference to the browser
        @type WebBrowserView
        @param url new URL
        @type QUrl
        """
        if browser == self.__mw.currentBrowser():
            self.currentChanged()
