# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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

from firsttimewizard import Ui_FirstTimeWizard

from openlp.core.lib import translate, PluginStatus
from openlp.core.utils import get_web_page, LanguageManager

log = logging.getLogger(__name__)

class FirstTimeForm(QtGui.QWizard, Ui_FirstTimeWizard):
    """
    This is the Theme Import Wizard, which allows easy creation and editing of
    OpenLP themes.
    """
    log.info(u'ThemeWizardForm loaded')

    def __init__(self, parent=None):
        # check to see if we have web access
        self.webAccess = get_web_page(u'http://openlp.org1')
        print self.webAccess
        QtGui.QWizard.__init__(self, parent)
        self.setupUi(self)
        #self.registerFields()

    def exec_(self, edit=False):
        """
        Run the wizard.
        """
        self.setDefaults()
        return QtGui.QWizard.exec_(self)

    def setDefaults(self):
        """
        Set up display at start of theme edit.
        """
        self.restart()
        # Sort out internet access
        if self.webAccess:
            self.internetGroupBox.setVisible(True)
            self.noInternetLabel.setVisible(False)
        else:
            self.internetGroupBox.setVisible(False)
            self.noInternetLabel.setVisible(True)
        self.qmList = LanguageManager.get_qm_list()
        for key in sorted(self.qmList.keys()):
            self.LanguageComboBox.addItem(key)

    def accept(self):
        self.__pluginStatus(self.songsCheckBox, u'songs/status')
        self.__pluginStatus(self.bibleCheckBox, u'bibles/status')
        self.__pluginStatus(self.presentationCheckBox, u'presentations/status')
        self.__pluginStatus(self.imageCheckBox, u'images/status')
        self.__pluginStatus(self.mediaCheckBox, u'media/status')
        self.__pluginStatus(self.remoteCheckBox, u'remote/status')
        self.__pluginStatus(self.customCheckBox, u'custom/status')
        self.__pluginStatus(self.songUsageCheckBox, u'songusage/status')
        self.__pluginStatus(self.alertCheckBox, u'alerts/status')

        print self.qmList[unicode(self.LanguageComboBox.currentText())]
        return QtGui.QWizard.accept(self)

    def __pluginStatus(self, field, tag):
        status = PluginStatus.Active if field.checkState() \
            == QtCore.Qt.Checked else PluginStatus.Inactive
        QtCore.QSettings().setValue(tag, QtCore.QVariant(status))
