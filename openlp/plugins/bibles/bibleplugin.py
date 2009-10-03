# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Plugin, translate, buildIcon
from openlp.plugins.bibles.lib import BibleManager, BiblesTab, BibleMediaItem

class BiblePlugin(Plugin):
    global log
    log = logging.getLogger(u'BiblePlugin')
    log.info(u'Bible Plugin loaded')

    def __init__(self, plugin_helpers):
        # Call the parent constructor
        Plugin.__init__(self, u'Bibles', u'1.9.0', plugin_helpers)
        self.weight = -9
        # Create the plugin icon
        self.icon = buildIcon(u':/media/media_bible.png')
        #Register the bible Manager
        self.biblemanager = BibleManager(self.config)

    def get_settings_tab(self):
        return BiblesTab()

    def get_media_manager_item(self):
        # Create the BibleManagerItem object
        return BibleMediaItem(self, self.icon, u'Bible Verses')

    def add_import_menu_item(self, import_menu):
        self.ImportBibleItem = QtGui.QAction(import_menu)
        self.ImportBibleItem.setObjectName(u'ImportBibleItem')
        import_menu.addAction(self.ImportBibleItem)
        self.ImportBibleItem.setText(translate(u'BiblePlugin', u'&Bible'))
        # Signals and slots
        QtCore.QObject.connect(self.ImportBibleItem,
            QtCore.SIGNAL(u'triggered()'), self.onBibleNewClick)

    def add_export_menu_item(self, export_menu):
        self.ExportBibleItem = QtGui.QAction(export_menu)
        self.ExportBibleItem.setObjectName(u'ExportBibleItem')
        export_menu.addAction(self.ExportBibleItem)
        self.ExportBibleItem.setText(translate(u'BiblePlugin', u'&Bible'))

    def onBibleNewClick(self):
        self.media_item.onBibleNewClick()

    def about(self):
        return u'<b>Bible Plugin</b> <br>This plugin allows bible verse from different sources to be displayed on the screen during the service.<br><br>This is a core plugin and cannot be made inactive</b>'
