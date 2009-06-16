"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

import random
import unittest

import os, os.path
import sys
mypath=os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..', '..','..','..')))

from openlp.plugins.biblemanager.bibleManager import BibleManager
from openlp.core.utils import ConfigHelper

import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')

console=logging.StreamHandler()
# set a format which is simpler for console use
formatter = logging.Formatter(u'%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
logging.getLogger(u'').addHandler(console)
log=logging.getLogger(u'')

logging.info(u'\nLogging started')

class TestBibleManager:
    log=logging.getLogger(u'testBibleMgr')
    def setup_class(self):
        log.debug(u'\n.......Register BM')
        self.bm = BibleManager()
           
    def testGetBibles(self):
        log.debug( "\n.......testGetBibles')
        # make sure the shuffled sequence does not lose any elements
        b = self.bm.getBibles()
        for b1 in b:
            log.debug( b1)
            assert(b1 in b)

    def testGetBibleBooks(self):
        log.debug( "\n.......testGetBibleBooks')
        c = self.bm.getBibleBooks(u'asv')
        for c1 in c:
            log.debug( c1)
            assert(c1 in c)
            
    def testGetBookChapterCount(self):
        log.debug( "\n.......testGetBookChapterCount')       
        assert(self.bm.getBookChapterCount(u'asv","Matthew')[0] == 28)

    def testGetBookVerseCount(self):
        log.debug( "\n.......testGetBookVerseCount')    
        assert(self.bm.getBookVerseCount(u'asv","Genesis", 1)[0] == 31)
        assert(self.bm.getBookVerseCount(u'TheMessage","Genesis", 2)[0] == 25)
        assert(self.bm.getBookVerseCount(u'asv","Matthew", 1)[0] == 25)
        assert(self.bm.getBookVerseCount(u'TheMessage","Revelation", 1)[0] == 20)        

    def testGetVerseText(self):
        log.debug( "\n.......testGetVerseText')
        #c = self.bm.getVerseText(u'TheMessage",'Genesis',1,2,1)
        #log.debug( c )
        #c = self.bm.getVerseText(u'NIV','Genesis',1,1,2)
        #log.debug( c ) 
        c = self.bm.getVerseText(u'asv','Genesis',10,1,20)
        log.debug( c )
        c = self.bm.getVerseText(u'TheMessage','Genesis',10,1,20)
        log.debug( c )       
        c = self.bm.getVerseText(u'asv','Revelation',10,1,20)
        log.debug( c ) 
        c = self.bm.getVersesFromText(u'asv", u'Jesus wept')
        log.debug( c )   
        c = self.bm.getVersesFromText(u'TheMessage", u'Jesus wept')
        log.debug( c )          