# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

from PyQt4 import QtCore, QtGui

class Ui_OpenLPExportDialog(object):
    def setupUi(self, OpenLPExportDialog):
        OpenLPExportDialog.setObjectName(u'OpenLPExportDialog')
        OpenLPExportDialog.resize(473, 459)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(u':/icon/openlp.org-icon-32.bmp'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        OpenLPExportDialog.setWindowIcon(icon)
        self.verticalLayout_5 = QtGui.QVBoxLayout(OpenLPExportDialog)
        self.verticalLayout_5.setMargin(8)
        self.verticalLayout_5.setObjectName(u'verticalLayout_5')
        self.ExportFileWidget = QtGui.QWidget(OpenLPExportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ExportFileWidget.sizePolicy().hasHeightForWidth())
        self.ExportFileWidget.setSizePolicy(sizePolicy)
        self.ExportFileWidget.setObjectName(u'ExportFileWidget')
        self.horizontalLayout = QtGui.QHBoxLayout(self.ExportFileWidget)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        self.ExportFileLabel = QtGui.QLabel(self.ExportFileWidget)
        self.ExportFileLabel.setObjectName(u'ExportFileLabel')
        self.horizontalLayout.addWidget(self.ExportFileLabel)
        self.ExportFileLineEdit = QtGui.QLineEdit(self.ExportFileWidget)
        self.ExportFileLineEdit.setObjectName(u'ExportFileLineEdit')
        self.horizontalLayout.addWidget(self.ExportFileLineEdit)
        self.ExportFileSelectPushButton = QtGui.QPushButton(self.ExportFileWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(u':/exports/export_load.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ExportFileSelectPushButton.setIcon(icon1)
        self.ExportFileSelectPushButton.setObjectName(u'ExportFileSelectPushButton')
        self.horizontalLayout.addWidget(self.ExportFileSelectPushButton)
        self.verticalLayout_5.addWidget(self.ExportFileWidget)
        self.SongListFrame = QtGui.QFrame(OpenLPExportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SongListFrame.sizePolicy().hasHeightForWidth())
        self.SongListFrame.setSizePolicy(sizePolicy)
        self.SongListFrame.setFrameShape(QtGui.QFrame.Box)
        self.SongListFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.SongListFrame.setObjectName(u'SongListFrame')
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.SongListFrame)
        self.horizontalLayout_6.setSpacing(8)
        self.horizontalLayout_6.setMargin(8)
        self.horizontalLayout_6.setObjectName(u'horizontalLayout_6')
        self.ExportFileSongListWidget = QtGui.QWidget(self.SongListFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ExportFileSongListWidget.sizePolicy().hasHeightForWidth())
        self.ExportFileSongListWidget.setSizePolicy(sizePolicy)
        self.ExportFileSongListWidget.setObjectName(u'ExportFileSongListWidget')
        self.verticalLayout = QtGui.QVBoxLayout(self.ExportFileSongListWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.ExportListLabel = QtGui.QLabel(self.ExportFileSongListWidget)
        self.ExportListLabel.setObjectName(u'ExportListLabel')
        self.verticalLayout.addWidget(self.ExportListLabel)
        self.ExportListTable = QtGui.QTableWidget(self.ExportFileSongListWidget)
        self.ExportListTable.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.ExportListTable.setShowGrid(False)
        self.ExportListTable.setWordWrap(False)
        self.ExportListTable.setCornerButtonEnabled(False)
        self.ExportListTable.setObjectName(u'ExportListTable')
        self.ExportListTable.setColumnCount(2)
        self.ExportListTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.ExportListTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.ExportListTable.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.ExportListTable)
        self.ExportSelectAllWidget = QtGui.QWidget(self.ExportFileSongListWidget)
        self.ExportSelectAllWidget.setObjectName(u'ExportSelectAllWidget')
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.ExportSelectAllWidget)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(u'horizontalLayout_2')
        self.ExportSelectAllPushButton = QtGui.QPushButton(self.ExportSelectAllWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ExportSelectAllPushButton.sizePolicy().hasHeightForWidth())
        self.ExportSelectAllPushButton.setSizePolicy(sizePolicy)
        self.ExportSelectAllPushButton.setMinimumSize(QtCore.QSize(100, 0))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(u':/exports/export_selectall.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ExportSelectAllPushButton.setIcon(icon2)
        self.ExportSelectAllPushButton.setObjectName(u'ExportSelectAllPushButton')
        self.horizontalLayout_2.addWidget(self.ExportSelectAllPushButton)
        spacerItem = QtGui.QSpacerItem(89, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.ExportSelectAllWidget)
        self.exportFilterWidget = QtGui.QWidget(self.ExportFileSongListWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportFilterWidget.sizePolicy().hasHeightForWidth())
        self.exportFilterWidget.setSizePolicy(sizePolicy)
        self.exportFilterWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.exportFilterWidget.setObjectName(u'exportFilterWidget')
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.exportFilterWidget)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(u'horizontalLayout_3')
        self.ExportFilterComboBox = QtGui.QComboBox(self.exportFilterWidget)
        self.ExportFilterComboBox.setMinimumSize(QtCore.QSize(70, 0))
        self.ExportFilterComboBox.setObjectName(u'ExportFilterComboBox')
        self.ExportFilterComboBox.addItem(QtCore.QString())
        self.ExportFilterComboBox.addItem(QtCore.QString())
        self.ExportFilterComboBox.addItem(QtCore.QString())
        self.horizontalLayout_3.addWidget(self.ExportFilterComboBox)
        self.ExportFilterLineEdit = QtGui.QLineEdit(self.exportFilterWidget)
        self.ExportFilterLineEdit.setObjectName(u'ExportFilterLineEdit')
        self.horizontalLayout_3.addWidget(self.ExportFilterLineEdit)
        self.verticalLayout.addWidget(self.exportFilterWidget)
        self.horizontalLayout_6.addWidget(self.ExportFileSongListWidget)
        self.AddSelectedWidget = QtGui.QWidget(self.SongListFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddSelectedWidget.sizePolicy().hasHeightForWidth())
        self.AddSelectedWidget.setSizePolicy(sizePolicy)
        self.AddSelectedWidget.setObjectName(u'AddSelectedWidget')
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.AddSelectedWidget)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(u'verticalLayout_3')
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.AddSelectedPushButton = QtGui.QPushButton(self.AddSelectedWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddSelectedPushButton.sizePolicy().hasHeightForWidth())
        self.AddSelectedPushButton.setSizePolicy(sizePolicy)
        self.AddSelectedPushButton.setMinimumSize(QtCore.QSize(25, 25))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(u':/exports/export_move_to_list.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AddSelectedPushButton.setIcon(icon3)
        self.AddSelectedPushButton.setObjectName(u'AddSelectedPushButton')
        self.verticalLayout_3.addWidget(self.AddSelectedPushButton)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout_6.addWidget(self.AddSelectedWidget)
        self.SelectedFileListWidget = QtGui.QWidget(self.SongListFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectedFileListWidget.sizePolicy().hasHeightForWidth())
        self.SelectedFileListWidget.setSizePolicy(sizePolicy)
        self.SelectedFileListWidget.setObjectName(u'SelectedFileListWidget')
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.SelectedFileListWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(u'verticalLayout_2')
        self.SelectedListLabel = QtGui.QLabel(self.SelectedFileListWidget)
        self.SelectedListLabel.setObjectName(u'SelectedListLabel')
        self.verticalLayout_2.addWidget(self.SelectedListLabel)
        self.SelectedListTable = QtGui.QTableWidget(self.SelectedFileListWidget)
        self.SelectedListTable.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.SelectedListTable.setShowGrid(False)
        self.SelectedListTable.setWordWrap(False)
        self.SelectedListTable.setCornerButtonEnabled(False)
        self.SelectedListTable.setObjectName(u'SelectedListTable')
        self.SelectedListTable.setColumnCount(2)
        self.SelectedListTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.SelectedListTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.SelectedListTable.setHorizontalHeaderItem(1, item)
        self.verticalLayout_2.addWidget(self.SelectedListTable)
        self.SelectedSelectAllWidget = QtGui.QWidget(self.SelectedFileListWidget)
        self.SelectedSelectAllWidget.setObjectName(u'SelectedSelectAllWidget')
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.SelectedSelectAllWidget)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(u'horizontalLayout_4')
        self.SelectedSelectAllPushButton = QtGui.QPushButton(self.SelectedSelectAllWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectedSelectAllPushButton.sizePolicy().hasHeightForWidth())
        self.SelectedSelectAllPushButton.setSizePolicy(sizePolicy)
        self.SelectedSelectAllPushButton.setMinimumSize(QtCore.QSize(100, 0))
        self.SelectedSelectAllPushButton.setIcon(icon2)
        self.SelectedSelectAllPushButton.setObjectName(u'SelectedSelectAllPushButton')
        self.horizontalLayout_4.addWidget(self.SelectedSelectAllPushButton)
        spacerItem3 = QtGui.QSpacerItem(92, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout_2.addWidget(self.SelectedSelectAllWidget)
        self.SelectedRemoveSelectedWidget = QtGui.QWidget(self.SelectedFileListWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectedRemoveSelectedWidget.sizePolicy().hasHeightForWidth())
        self.SelectedRemoveSelectedWidget.setSizePolicy(sizePolicy)
        self.SelectedRemoveSelectedWidget.setObjectName(u'SelectedRemoveSelectedWidget')
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.SelectedRemoveSelectedWidget)
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setObjectName(u'horizontalLayout_5')
        self.SelectedRemoveSelectedButton = QtGui.QPushButton(self.SelectedRemoveSelectedWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectedRemoveSelectedButton.sizePolicy().hasHeightForWidth())
        self.SelectedRemoveSelectedButton.setSizePolicy(sizePolicy)
        self.SelectedRemoveSelectedButton.setMinimumSize(QtCore.QSize(140, 0))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(u':/exports/export_remove.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SelectedRemoveSelectedButton.setIcon(icon4)
        self.SelectedRemoveSelectedButton.setObjectName(u'SelectedRemoveSelectedButton')
        self.horizontalLayout_5.addWidget(self.SelectedRemoveSelectedButton)
        spacerItem4 = QtGui.QSpacerItem(49, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout_2.addWidget(self.SelectedRemoveSelectedWidget)
        self.horizontalLayout_6.addWidget(self.SelectedFileListWidget)
        self.verticalLayout_5.addWidget(self.SongListFrame)
        self.ProgressGroupBox = QtGui.QGroupBox(OpenLPExportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ProgressGroupBox.sizePolicy().hasHeightForWidth())
        self.ProgressGroupBox.setSizePolicy(sizePolicy)
        self.ProgressGroupBox.setObjectName(u'ProgressGroupBox')
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.ProgressGroupBox)
        self.verticalLayout_4.setSpacing(8)
        self.verticalLayout_4.setContentsMargins(8, 0, 8, 8)
        self.verticalLayout_4.setObjectName(u'verticalLayout_4')
        self.ProgressLabel = QtGui.QLabel(self.ProgressGroupBox)
        self.ProgressLabel.setObjectName(u'ProgressLabel')
        self.verticalLayout_4.addWidget(self.ProgressLabel)
        self.ProgressBar = QtGui.QProgressBar(self.ProgressGroupBox)
        self.ProgressBar.setProperty(u'value', QtCore.QVariant(24))
        self.ProgressBar.setObjectName(u'ProgressBar')
        self.verticalLayout_4.addWidget(self.ProgressBar)
        self.verticalLayout_5.addWidget(self.ProgressGroupBox)
        self.ButtonBarWidget = QtGui.QWidget(OpenLPExportDialog)
        self.ButtonBarWidget.setObjectName(u'ButtonBarWidget')
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.ButtonBarWidget)
        self.horizontalLayout_7.setSpacing(8)
        self.horizontalLayout_7.setMargin(0)
        self.horizontalLayout_7.setObjectName(u'horizontalLayout_7')
        spacerItem5 = QtGui.QSpacerItem(288, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem5)
        self.ExportPushButton = QtGui.QPushButton(self.ButtonBarWidget)
        self.ExportPushButton.setObjectName(u'ExportPushButton')
        self.horizontalLayout_7.addWidget(self.ExportPushButton)
        self.ClosePushButton = QtGui.QPushButton(self.ButtonBarWidget)
        self.ClosePushButton.setObjectName(u'ClosePushButton')
        self.horizontalLayout_7.addWidget(self.ClosePushButton)
        self.verticalLayout_5.addWidget(self.ButtonBarWidget)

        self.retranslateUi(OpenLPExportDialog)
        QtCore.QObject.connect(self.ClosePushButton, QtCore.SIGNAL(u'clicked()'), OpenLPExportDialog.close)
        QtCore.QObject.connect(self.ExportSelectAllPushButton, QtCore.SIGNAL(u'clicked()'), self.ExportListTable.selectAll)
        QtCore.QObject.connect(self.SelectedSelectAllPushButton, QtCore.SIGNAL(u'clicked()'), self.SelectedListTable.selectAll)
        QtCore.QObject.connect(self.SelectedRemoveSelectedButton, QtCore.SIGNAL(u'clicked()'), self.SelectedListTable.clear)
        QtCore.QMetaObject.connectSlotsByName(OpenLPExportDialog)

    def retranslateUi(self, OpenLPExportDialog):
        OpenLPExportDialog.setWindowTitle(self.trUtf8('openlp.org Song Exporter'))
        self.ExportFileLabel.setText(self.trUtf8('Select openlp.org export filename:'))
        self.ExportListLabel.setText(self.trUtf8('Full Song List'))
        self.ExportListTable.horizontalHeaderItem(0).setText(self.trUtf8('Song Title'))
        self.ExportListTable.horizontalHeaderItem(1).setText(self.trUtf8('Author'))
        self.ExportSelectAllPushButton.setText(self.trUtf8('Select All'))
        self.ExportFilterComboBox.setItemText(0, self.trUtf8('Lyrics'))
        self.ExportFilterComboBox.setItemText(1, self.trUtf8('Title'))
        self.ExportFilterComboBox.setItemText(2, self.trUtf8('Author'))
        self.SelectedListLabel.setText(self.trUtf8('Song Export List'))
        self.SelectedListTable.horizontalHeaderItem(0).setText(self.trUtf8('Song Title'))
        self.SelectedListTable.horizontalHeaderItem(1).setText(self.trUtf8('Author'))
        self.SelectedSelectAllPushButton.setText(self.trUtf8('Select All'))
        self.SelectedRemoveSelectedButton.setText(self.trUtf8('Remove Selected'))
        self.ProgressGroupBox.setTitle(self.trUtf8('Progress:'))
        self.ProgressLabel.setText(self.trUtf8('Ready to export'))
        self.ExportPushButton.setText(self.trUtf8('Export'))
        self.ClosePushButton.setText(self.trUtf8('Close'))
