# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

# OOo API documentation:
# http://wiki.services.openoffice.org/wiki/Documentation/BASIC_Guide/Structure_of_Text_Documents
# http://wiki.services.openoffice.org/wiki/Documentation/DevGuide/Text/Iterating_over_Text
# http://www.oooforum.org/forum/viewtopic.phtml?t=14409
# http://wiki.services.openoffice.org/wiki/Python

import re
import os
import time
from PyQt4 import QtCore

if os.name == u'nt':
    from win32com.client import Dispatch
    BOLD = 150.0
    ITALIC = 2
    PAGE_BEFORE = 4
    PAGE_AFTER = 5
    PAGE_BOTH = 6
else:
    import uno
    from com.sun.star.beans import PropertyValue
    from com.sun.star.awt.FontWeight import BOLD
    from com.sun.star.awt.FontSlant import ITALIC
    from com.sun.star.style.BreakType import PAGE_BEFORE, PAGE_AFTER, PAGE_BOTH

class sofimport:
    def __init__(self):
        self.song = None
        self.new_song()

    def start_ooo(self):
        if os.name == u'nt':
            manager = Dispatch(u'com.sun.star.ServiceManager')
            manager._FlagAsMethod(u'Bridge_GetStruct')
            manager._FlagAsMethod(u'Bridge_GetValueObject')
            self.desktop = manager.createInstance(u'com.sun.star.frame.Desktop')
        else:
            cmd = u'openoffice.org -nologo -norestore -minimized -invisible -nofirststartwizard -accept="socket,host=localhost,port=2002;urp;"'
            process = QtCore.QProcess()
            process.startDetached(cmd)
            process.waitForStarted()
            context = uno.getComponentContext()
            resolver = context.ServiceManager.createInstanceWithContext(
                u'com.sun.star.bridge.UnoUrlResolver', context)
            ctx = None
            loop = 0
            while ctx is None and loop < 3:
                try:
                    ctx = resolver.resolve(u'uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext')
                except:
                    time.sleep(1)
                    loop += 1
            manager = ctx.ServiceManager
            self.desktop = manager.createInstanceWithContext(
                "com.sun.star.frame.Desktop", ctx )
            
    def open_sof_file(self, filepath):
        if os.name == u'nt':
            url = u'file:///' + filepath.replace(u'\\', u'/')
            url = url.replace(u':', u'|').replace(u' ', u'%20')
        else:
            url = uno.systemPathToFileUrl(filepath)
        properties = []
        properties = tuple(properties)
        self.document = self.desktop.loadComponentFromURL(url, u'_blank',
            0, properties)

    def close_ooo(self):
        self.desktop.terminate()

    def process_doc(self):
        self.blanklines = 0
        paragraphs = self.document.getText().createEnumeration()
        while paragraphs.hasMoreElements():
            paragraph = paragraphs.nextElement()
            if paragraph.supportsService("com.sun.star.text.Paragraph"):
                self.process_paragraph(paragraph)
        if self.song:
            self.song.finish()
            self.song = None

    def process_paragraph(self, paragraph):
        text = u''
        textportions = paragraph.createEnumeration()
        while textportions.hasMoreElements():
            textportion = textportions.nextElement()
            if textportion.BreakType in (PAGE_BEFORE, PAGE_BOTH):
                self.process_paragraph_text(text)
                self.new_song()
                text = u''
            text += self.process_textportion(textportion)
            if textportion.BreakType in (PAGE_AFTER, PAGE_BOTH):
                self.process_paragraph_text(text)
                self.new_song()
                text = u''
        self.process_paragraph_text(text)
        
    def process_paragraph_text(self, text):
        for line in text.split(u'\n'):
            self.process_paragraph_line(line)
        if self.blanklines > 2:
            self.new_song()

    def process_paragraph_line(self, text):
        text = text.strip()        
        if text == u'':
            self.blanklines += 1
            if self.blanklines > 1:
                return
            if self.song.title != u'':
                self.song.finish_verse()
            return
        #print ">" + text + "<"
        self.blanklines = 0
        if self.skip_to_close_bracket:
            if text.endswith(u')'):
                self.skip_to_close_bracket = False
            return 
        if text.startswith(u'CCL Licence'):
            self.in_chorus = False
            return
        if text == u'A Songs of Fellowship Worship Resource':
            return
        if text.startswith(u'(NB.') or text.startswith(u'(Regrettably') \
            or text.startswith(u'(From'):
            self.skip_to_close_bracket = True
            return
        if text.startswith(u'Copyright'):
            self.song.copyright = text
            return
        if text == u'(Repeat)':
            self.song.repeat_verse()
            return
        if self.song.title == u'':
            if self.song.copyright == u'':
                self.song.add_author(text)
            else:
                self.song.copyright += u' ' + text
            return
        self.song.add_verse_line(text, self.in_chorus)

    def process_textportion(self, textportion):
        text = textportion.getString()
        text = self.tidy_text(text)
        if text.strip() == u'':
            return text
        if textportion.CharWeight == BOLD:
            boldtext = text.strip()
            if boldtext.isdigit() and self.song.songnumber == 0:
                self.song.songnumber = int(boldtext)
                return u''
            if self.song.title == u'':
                text = self.uncap_text(text)
                title = text.strip()
                if title.startswith(u'\''):
                    title = title[1:]
                if title.endswith(u','):
                    title = title[:-1]
                self.song.title = title
            return text
        if text.strip().startswith(u'('):
            return text
        self.in_chorus = (textportion.CharPosture == ITALIC)
        return text

    def new_song(self):
        if self.song:
            if not self.song.finish():
                return
        self.song = sofsong()
        self.skip_to_close_bracket = False
        self.in_chorus = False

    def tidy_text(self, text):
        text = text.replace(u'\t', u' ')
        text = text.replace(u'\r', u'\n')
        text = text.replace(u'\u2018', u'\'')
        text = text.replace(u'\u2019', u'\'')
        text = text.replace(u'\u201c', u'"')
        text = text.replace(u'\u201d', u'"')
        text = text.replace(u'\u2026', u'...')
        text = text.replace(u'\u2013', u'-')
        text = text.replace(u'\u2014', u'-')
        return text

    def uncap_text(self, text):
        textarr = re.split(u'(\W+)', text)
        textarr[0] = textarr[0].capitalize()
        for i in range(1, len(textarr)):
            # Do not translate these. Fixed strings in SOF song file
            if textarr[i] in (u'JESUS', u'CHRIST', u'KING', u'ALMIGHTY', 
                u'REDEEMER', u'SHEPHERD', u'SON', u'GOD', u'LORD', u'FATHER', 
                u'HOLY', u'SPIRIT', u'LAMB', u'YOU', u'YOUR', u'I', u'I\'VE', 
                u'I\'M', u'I\'LL', u'SAVIOUR', u'O', u'YOU\'RE', u'HE', u'HIS', 
                u'HIM', u'ZION', u'EMMANUEL', u'MAJESTY', u'JESUS\'', u'JIREH', 
                u'JUDAH', u'LION', u'LORD\'S', u'ABRAHAM', u'GOD\'S', 
                u'FATHER\'S', u'ELIJAH'):
                textarr[i] = textarr[i].capitalize()
            else:
                textarr[i] = textarr[i].lower()
        text = u''.join(textarr)
        return text

class sofsong:
    def __init__(self):
        self.songnumber = 0
        self.title = u''
        self.ischorus = False
        self.versecount = 0
        self.choruscount = 0
        self.verses = []
        self.order = []
        self.authors = []
        self.copyright = u''
        self.book = u''
        self.currentverse = u''

    def finish_verse(self):
        if self.currentverse.strip() == u'':
            return
        if self.ischorus:
            splitat = None
        else:
            splitat = self.verse_splits()
        if splitat:
            ln = 0
            verse = u''
            for line in self.currentverse.split(u'\n'):
                ln += 1
                if line == u'' or ln > splitat:
                    self.append_verse(verse)
                    ln = 0
                    if line:
                        verse = line + u'\n'
                    else:   
                        verse = u''
                else:
                    verse += line + u'\n'
            if verse:
                self.append_verse(verse)
        else:
            self.append_verse(self.currentverse)
        self.currentverse = u''
        self.ischorus = False

    def append_verse(self, verse):
        if self.ischorus:
            self.choruscount += 1
            versetag = u'C' + unicode(self.choruscount)
        else:
            self.versecount += 1
            versetag = u'V' + unicode(self.versecount)
        self.verses.append([versetag, verse])
        self.order.append(versetag)
        if self.choruscount > 0 and not self.ischorus:
            self.order.append(u'C' + unicode(self.choruscount))

    def repeat_verse(self):
        self.finish_verse()
        self.order.append(self.order[-1])

    def add_verse_line(self, text, inchorus):
        if inchorus != self.ischorus and ((len(self.verses) > 0) or 
            (self.currentverse.count(u'\n') > 1)):
            self.finish_verse()
        if inchorus:
            self.ischorus = True
        self.currentverse += text + u'\n'
    
    def add_author(self, text):
        text = text.replace(u' and ', u' & ')
        for author in text.split(u','):
            authors = author.split(u'&')
            for i in range(len(authors)):
                author2 = authors[i].strip()
                if author2.find(u' ') == -1 and i < len(authors) - 1:
                    author2 = author2 + u' ' + authors[i + 1].split(u' ')[-1]
                self.authors.append(author2)
        
    def finish(self):
        self.finish_verse()
        if self.songnumber == 0  \
            or self.title == u''  \
            or len(self.verses) == 0:
            return False
        if len(self.authors) == 0:
            self.authors.append(u'Author Unknown')
        if self.songnumber <= 640:
            self.book = u'Songs of Fellowship 1'
        elif self.songnumber <= 1150:
            self.book = u'Songs of Fellowship 2'
        elif self.songnumber <= 1690:
            self.book = u'Songs of Fellowship 3'
        else:
            self.book = u'Songs of Fellowship 4'
        self.print_song()
        return True
        
    def print_song(self):
        print u'===== TITLE: ' + self.title + u' ====='
        print u'ALTTITLE: ' + unicode(self.songnumber)
        for (verselabel, verse) in self.verses:
            print u'VERSE ' + verselabel + u': ' + verse
        print u'ORDER: ' + unicode(self.order)
        for author in self.authors:
            print u'AUTHORS: ' + author
        print u'COPYRIGHT: ' + self.copyright
        print u'BOOK: ' + self.book

    def verse_splits(self):
        """
        Because someone at Kingsway forgot to check the 1+2 RTF file, 
        some verses were not formatted correctly.
        """
        if self.songnumber == 11: return 8
        if self.songnumber == 18: return 5
        if self.songnumber == 21: return 6
        if self.songnumber == 23: return 4
        if self.songnumber == 24: return 7
        if self.songnumber == 27: return 4
        if self.songnumber == 31: return 6
        if self.songnumber == 49: return 4
        if self.songnumber == 50: return 8
        if self.songnumber == 70: return 4	
        if self.songnumber == 75: return 8
        if self.songnumber == 79: return 6
        if self.songnumber == 97: return 7
        if self.songnumber == 107: return 4
        if self.songnumber == 109: return 4
        if self.songnumber == 133: return 4
        if self.songnumber == 155: return 10
        if self.songnumber == 156: return 8
        if self.songnumber == 171: return 4
        if self.songnumber == 188: return 7
        if self.songnumber == 192: return 4
        if self.songnumber == 208: return 8
        if self.songnumber == 215: return 8
        if self.songnumber == 220: return 4
        if self.songnumber == 247: return 6
        if self.songnumber == 248: return 6
        if self.songnumber == 251: return 8
        if self.songnumber == 295: return 8
        if self.songnumber == 307: return 5
        if self.songnumber == 314: return 6
        if self.songnumber == 325: return 8
        if self.songnumber == 386: return 6
        if self.songnumber == 415: return 4
        if self.songnumber == 426: return 4
        if self.songnumber == 434: return 5
        if self.songnumber == 437: return 4
        if self.songnumber == 438: return 6
        if self.songnumber == 456: return 8
        if self.songnumber == 461: return 4
        if self.songnumber == 469: return 4
        if self.songnumber == 470: return 5
        if self.songnumber == 476: return 6
        if self.songnumber == 477: return 7
        if self.songnumber == 480: return 8
        if self.songnumber == 482: return 4
        if self.songnumber == 512: return 4
        if self.songnumber == 513: return 8
        if self.songnumber == 518: return 5
        if self.songnumber == 520: return 4
        if self.songnumber == 523: return 6
        if self.songnumber == 526: return 8
        if self.songnumber == 527: return 4
        if self.songnumber == 529: return 4
        if self.songnumber == 537: return 4
        if self.songnumber == 555: return 6
        if self.songnumber == 581: return 4
        if self.songnumber == 589: return 6
        if self.songnumber == 590: return 4
        if self.songnumber == 593: return 8
        if self.songnumber == 596: return 4
        if self.songnumber == 610: return 6
        if self.songnumber == 611: return 6
        if self.songnumber == 619: return 8
        if self.songnumber == 645: return 5
        if self.songnumber == 653: return 6
        if self.songnumber == 683: return 7
        if self.songnumber == 686: return 4
        if self.songnumber == 697: return 8
        if self.songnumber == 698: return 4
        if self.songnumber == 704: return 6
        if self.songnumber == 716: return 4
        if self.songnumber == 717: return 6
        if self.songnumber == 730: return 4
        if self.songnumber == 731: return 8
        if self.songnumber == 732: return 8
        if self.songnumber == 738: return 4
        if self.songnumber == 756: return 9
        if self.songnumber == 815: return 6
        if self.songnumber == 830: return 8
        if self.songnumber == 831: return 4
        if self.songnumber == 876: return 6
        if self.songnumber == 877: return 6
        if self.songnumber == 892: return 4
        if self.songnumber == 894: return 6
        if self.songnumber == 902: return 8
        if self.songnumber == 905: return 8
        if self.songnumber == 921: return 6
        if self.songnumber == 940: return 7
        if self.songnumber == 955: return 9
        if self.songnumber == 968: return 8		
        if self.songnumber == 972: return 7
        if self.songnumber == 974: return 4
        if self.songnumber == 988: return 6
        if self.songnumber == 991: return 5
        if self.songnumber == 1002: return 8
        if self.songnumber == 1024: return 8
        if self.songnumber == 1044: return 9
        if self.songnumber == 1088: return 6
        if self.songnumber == 1117: return 6
        if self.songnumber == 1119: return 7
        return None

sof = sofimport()
sof.start_ooo()
sof.open_sof_file(u'/home/jonathan/sof.rtf')
#sof.open_sof_file(u'c:\users\jonathan\Desktop\sof3words.rtf')
#sof.open_sof_file(u'c:\users\jonathan\Desktop\sof4words.rtf')
sof.process_doc()
sof.close_ooo()

