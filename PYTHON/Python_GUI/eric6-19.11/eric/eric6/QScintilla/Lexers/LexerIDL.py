# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2019 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing an IDL lexer with some additional methods.
"""


from PyQt5.Qsci import QsciLexerIDL, QsciScintilla

from .Lexer import Lexer
import Preferences


class LexerIDL(Lexer, QsciLexerIDL):
    """
    Subclass to implement some additional lexer dependant methods.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent parent widget of this lexer
        """
        QsciLexerIDL.__init__(self, parent)
        Lexer.__init__(self)
        
        self.commentString = "//"
        self.streamCommentString = {
            'start': '/* ',
            'end': ' */'
        }
        self.boxCommentString = {
            'start': '/* ',
            'middle': ' * ',
            'end': ' */'
        }
        
        self.keywordSetDescriptions = [
            self.tr("Primary keywords and identifiers"),
            self.tr("Secondary keywords and identifiers"),
            self.tr("Documentation comment keywords"),
            self.tr("Global classes and typedefs"),
            self.tr("Preprocessor definitions"),
            self.tr("Task marker and error marker keywords"),
        ]
    
    def initProperties(self):
        """
        Public slot to initialize the properties.
        """
        self.setFoldComments(Preferences.getEditor("CppFoldComment"))
        self.setFoldPreprocessor(Preferences.getEditor("CppFoldPreprocessor"))
        self.setFoldAtElse(Preferences.getEditor("CppFoldAtElse"))
        indentStyle = 0
        if Preferences.getEditor("CppIndentOpeningBrace"):
            indentStyle |= QsciScintilla.AiOpening
        if Preferences.getEditor("CppIndentClosingBrace"):
            indentStyle |= QsciScintilla.AiClosing
        self.setAutoIndentStyle(indentStyle)
        self.setFoldCompact(Preferences.getEditor("AllFoldCompact"))
    
    def isCommentStyle(self, style):
        """
        Public method to check, if a style is a comment style.
        
        @param style style to check (integer)
        @return flag indicating a comment style (boolean)
        """
        return style in [QsciLexerIDL.Comment,
                         QsciLexerIDL.CommentDoc,
                         QsciLexerIDL.CommentLine,
                         QsciLexerIDL.CommentLineDoc]
    
    def isStringStyle(self, style):
        """
        Public method to check, if a style is a string style.
        
        @param style style to check (integer)
        @return flag indicating a string style (boolean)
        """
        return style in [QsciLexerIDL.DoubleQuotedString,
                         QsciLexerIDL.SingleQuotedString,
                         QsciLexerIDL.UnclosedString,
                         QsciLexerIDL.VerbatimString]
    
    def defaultKeywords(self, kwSet):
        """
        Public method to get the default keywords.
        
        @param kwSet number of the keyword set (integer)
        @return string giving the keywords (string) or None
        """
        return QsciLexerIDL.keywords(self, kwSet)
    
    def maximumKeywordSet(self):
        """
        Public method to get the maximum keyword set.
        
        @return maximum keyword set (integer)
        """
        return 4
