# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2019 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a specialized tab bar for the web browser.
"""


from PyQt5.QtCore import Qt, QPoint, QTimer, QEvent
from PyQt5.QtWidgets import QFrame, QLabel

from E5Gui.E5TabWidget import E5WheelTabBar
from E5Gui.E5PassivePopup import E5PassivePopup

import Preferences


class WebBrowserTabBar(E5WheelTabBar):
    """
    Class implementing the tab bar of the web browser.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (WebBrowserTabWidget)
        """
        super(WebBrowserTabBar, self).__init__(parent)
        
        self.__tabWidget = parent
        
        self.__previewPopup = None
        
        self.setMouseTracking(True)
    
    def __showTabPreview(self, index):
        """
        Private slot to show the tab preview.
        
        @param index index of tab to show a preview for
        @type int
        """
        indexedBrowser = self.__tabWidget.browserAt(index)
        currentBrowser = self.__tabWidget.currentBrowser()
        
        if indexedBrowser is None or currentBrowser is None:
            return
        
        # no previews during load
        if indexedBrowser.progress() != 0:
            return
        
        preview = indexedBrowser.getPreview()
        if not preview.isNull():
            w = self.tabSizeHint(index).width()
            h = int(w * currentBrowser.height() / currentBrowser.width())
            
            self.__previewPopup = E5PassivePopup(self)
            self.__previewPopup.setFrameShape(QFrame.StyledPanel)
            self.__previewPopup.setFrameShadow(QFrame.Plain)
            self.__previewPopup.setFixedSize(w, h)
            self.__previewPopup.setCustomData("index", index)
            
            label = QLabel()
            label.setPixmap(preview.scaled(w, h))
            
            self.__previewPopup.setView(label)
            self.__previewPopup.layout().setAlignment(Qt.AlignTop)
            self.__previewPopup.layout().setContentsMargins(0, 0, 0, 0)
            
            tr = self.tabRect(index)
            pos = QPoint(tr.x(), tr.y() + tr.height())
            
            self.__previewPopup.show(self.mapToGlobal(pos))
    
    def __hidePreview(self):
        """
        Private method to hide the preview.
        """
        if self.__previewPopup is not None:
            self.__previewPopup.hide()
        self.__previewPopup = None
    
    def mouseMoveEvent(self, evt):
        """
        Protected method to handle mouse move events.
        
        @param evt reference to the mouse move event (QMouseEvent)
        """
        if self.count() == 1:
            return
        
        super(WebBrowserTabBar, self).mouseMoveEvent(evt)
        
        if Preferences.getWebBrowser("ShowPreview"):
            # Find the tab under the mouse
            i = 0
            tabIndex = -1
            while i < self.count() and tabIndex == -1:
                if self.tabRect(i).contains(evt.pos()):
                    tabIndex = i
                i += 1
            
            # If found and not the current tab then show tab preview
            if (
                tabIndex != -1 and
                tabIndex != self.currentIndex() and
                evt.buttons() == Qt.NoButton
            ):
                if (
                    self.__previewPopup is None or
                    (self.__previewPopup is not None and
                     self.__previewPopup.getCustomData("index") != tabIndex)
                ):
                    QTimer.singleShot(
                        0, lambda: self.__showTabPreview(tabIndex))
            
            # If current tab or not found then hide previous tab preview
            if (
                tabIndex == self.currentIndex() or
                tabIndex == -1
            ):
                self.__hidePreview()
    
    def leaveEvent(self, evt):
        """
        Protected method to handle leave events.
        
        @param evt reference to the leave event (QEvent)
        """
        if Preferences.getWebBrowser("ShowPreview"):
            # If leave tabwidget then hide previous tab preview
            self.__hidePreview()
        
        super(WebBrowserTabBar, self).leaveEvent(evt)
    
    def mousePressEvent(self, evt):
        """
        Protected method to handle mouse press events.
        
        @param evt reference to the mouse press event (QMouseEvent)
        """
        if Preferences.getWebBrowser("ShowPreview"):
            self.__hidePreview()
        
        super(WebBrowserTabBar, self).mousePressEvent(evt)
    
    def event(self, evt):
        """
        Public method to handle event.
        
        This event handler just handles the tooltip event and passes the
        handling of all others to the superclass.
        
        @param evt reference to the event to be handled (QEvent)
        @return flag indicating, if the event was handled (boolean)
        """
        if (
            evt.type() == QEvent.ToolTip and
            Preferences.getWebBrowser("ShowPreview")
        ):
            # suppress tool tips if we are showing previews
            evt.setAccepted(True)
            return True
        
        return super(WebBrowserTabBar, self).event(evt)
    
    def tabRemoved(self, index):
        """
        Public slot to handle the removal of a tab.
        
        @param index index of the removed tab (integer)
        """
        if Preferences.getWebBrowser("ShowPreview"):
            self.__hidePreview()
