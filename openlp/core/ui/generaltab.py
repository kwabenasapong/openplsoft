# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 - 2009 Martin Thompson, Tim Bentley,

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

from PyQt4 import QtCore, QtGui

from openlp.core import translate
from openlp.core.lib import SettingsTab
from openlp.core.resources import *

class GeneralTab(SettingsTab):
    """
    GeneralTab is the general settings tab in the settings dialog.
    """
    def __init__(self):
        SettingsTab.__init__(self, translate(u'GeneralTab', u'General'))

    def setupUi(self):
        self.setObjectName(u'GeneralTab')
        self.GeneralLayout = QtGui.QHBoxLayout(self)
        self.GeneralLayout.setSpacing(8)
        self.GeneralLayout.setMargin(8)
        self.GeneralLayout.setObjectName(u'GeneralLayout')
        self.GeneralLeftWidget = QtGui.QWidget(self)
        self.GeneralLeftWidget.setObjectName(u'GeneralLeftWidget')
        self.GeneralLeftLayout = QtGui.QVBoxLayout(self.GeneralLeftWidget)
        self.GeneralLeftLayout.setObjectName(u'GeneralLeftLayout')
        self.GeneralLeftLayout.setSpacing(8)
        self.GeneralLeftLayout.setMargin(0)
        self.MonitorGroupBox = QtGui.QGroupBox(self.GeneralLeftWidget)
        self.MonitorGroupBox.setObjectName(u'MonitorGroupBox')
        self.MonitorLayout = QtGui.QVBoxLayout(self.MonitorGroupBox)
        self.MonitorLayout.setSpacing(8)
        self.MonitorLayout.setMargin(8)
        self.MonitorLayout.setObjectName(u'MonitorLayout')
        self.MonitorLabel = QtGui.QLabel(self.MonitorGroupBox)
        self.MonitorLabel.setObjectName(u'MonitorLabel')
        self.MonitorLayout.addWidget(self.MonitorLabel)
        self.MonitorComboBox = QtGui.QComboBox(self.MonitorGroupBox)
        self.MonitorComboBox.setObjectName(u'MonitorComboBox')
        self.MonitorComboBox.addItem(QtCore.QString())
        self.MonitorComboBox.addItem(QtCore.QString())
        self.MonitorLayout.addWidget(self.MonitorComboBox)
        self.GeneralLeftLayout.addWidget(self.MonitorGroupBox)
        self.BlankScreenGroupBox = QtGui.QGroupBox(self.GeneralLeftWidget)
        self.BlankScreenGroupBox.setObjectName(u'BlankScreenGroupBox')
        self.BlankScreenLayout = QtGui.QVBoxLayout(self.BlankScreenGroupBox)
        self.BlankScreenLayout.setSpacing(8)
        self.BlankScreenLayout.setMargin(8)
        self.BlankScreenLayout.setObjectName(u'BlankScreenLayout')
        self.WarningCheckBox = QtGui.QCheckBox(self.BlankScreenGroupBox)
        self.WarningCheckBox.setObjectName(u'WarningCheckBox')
        self.BlankScreenLayout.addWidget(self.WarningCheckBox)
        self.GeneralLeftLayout.addWidget(self.BlankScreenGroupBox)
        self.AutoOpenGroupBox = QtGui.QGroupBox(self.GeneralLeftWidget)
        self.AutoOpenGroupBox.setObjectName(u'AutoOpenGroupBox')
        self.AutoOpenLayout = QtGui.QVBoxLayout(self.AutoOpenGroupBox)
        self.AutoOpenLayout.setObjectName(u'AutoOpenLayout')
        self.AutoOpenCheckBox = QtGui.QCheckBox(self.AutoOpenGroupBox)
        self.AutoOpenCheckBox.setObjectName(u'AutoOpenCheckBox')
        self.AutoOpenLayout.addWidget(self.AutoOpenCheckBox)
        self.GeneralLeftLayout.addWidget(self.AutoOpenGroupBox)
        self.GeneralLeftSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.GeneralLeftLayout.addItem(self.GeneralLeftSpacer)
        self.GeneralLayout.addWidget(self.GeneralLeftWidget)
        self.GeneralRightWidget = QtGui.QWidget(self)
        self.GeneralRightWidget.setObjectName(u'GeneralRightWidget')
        self.GeneralRightLayout = QtGui.QVBoxLayout(self.GeneralRightWidget)
        self.GeneralRightLayout.setSpacing(8)
        self.GeneralRightLayout.setMargin(0)
        self.GeneralRightLayout.setObjectName(u'GeneralRightLayout')
        self.CCLIGroupBox = QtGui.QGroupBox(self.GeneralRightWidget)
        self.CCLIGroupBox.setObjectName(u'CCLIGroupBox')
        self.CCLILayout = QtGui.QGridLayout(self.CCLIGroupBox)
        self.CCLILayout.setMargin(8)
        self.CCLILayout.setSpacing(8)
        self.CCLILayout.setObjectName(u'CCLILayout')
        self.NumberLabel = QtGui.QLabel(self.CCLIGroupBox)
        self.NumberLabel.setObjectName(u'NumberLabel')
        self.CCLILayout.addWidget(self.NumberLabel, 0, 0, 1, 1)
        self.NumberEdit = QtGui.QLineEdit(self.CCLIGroupBox)
        self.NumberEdit.setObjectName(u'NumberEdit')
        self.CCLILayout.addWidget(self.NumberEdit, 0, 1, 1, 1)
        self.UsernameLabel = QtGui.QLabel(self.CCLIGroupBox)
        self.UsernameLabel.setObjectName(u'UsernameLabel')
        self.CCLILayout.addWidget(self.UsernameLabel, 1, 0, 1, 1)
        self.UsernameEdit = QtGui.QLineEdit(self.CCLIGroupBox)
        self.UsernameEdit.setObjectName(u'UsernameEdit')
        self.CCLILayout.addWidget(self.UsernameEdit, 1, 1, 1, 1)
        self.PasswordLabel = QtGui.QLabel(self.CCLIGroupBox)
        self.PasswordLabel.setObjectName(u'PasswordLabel')
        self.CCLILayout.addWidget(self.PasswordLabel, 2, 0, 1, 1)
        self.PasswordEdit = QtGui.QLineEdit(self.CCLIGroupBox)
        self.PasswordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.PasswordEdit.setObjectName(u'PasswordEdit')
        self.CCLILayout.addWidget(self.PasswordEdit, 2, 1, 1, 1)
        self.GeneralRightLayout.addWidget(self.CCLIGroupBox)
        self.GeneralRightSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.GeneralRightLayout.addItem(self.GeneralRightSpacer)
        self.GeneralLayout.addWidget(self.GeneralRightWidget)

    def retranslateUi(self):
        self.MonitorGroupBox.setTitle(translate(u'GeneralTab', u'Monitors'))
        self.MonitorLabel.setText(translate(u'GeneralTab', u'Select monitor for output display:'))
        self.MonitorComboBox.setItemText(0, translate(u'GeneralTab', u'Monitor 1 on X11 Windowing System'))
        self.MonitorComboBox.setItemText(1, translate(u'GeneralTab', u'Monitor 2 on X11 Windowing System'))
        self.BlankScreenGroupBox.setTitle(translate(u'GeneralTab', u'Blank Screen'))
        self.WarningCheckBox.setText(translate(u'GeneralTab', u'Show warning on startup'))
        self.AutoOpenGroupBox.setTitle(translate(u'GeneralTab', u'Auto Open Last Service'))
        self.AutoOpenCheckBox.setText(translate(u'GeneralTab', u'Automatically open the last service at startup'))
        self.CCLIGroupBox.setTitle(translate(u'GeneralTab', u'CCLI Details'))
        self.NumberLabel.setText(translate(u'GeneralTab', u'CCLI Number:'))
        self.UsernameLabel.setText(translate(u'GeneralTab', u'SongSelect Username:'))
        self.PasswordLabel.setText(translate(u'GeneralTab', u'SongSelect Password:'))

