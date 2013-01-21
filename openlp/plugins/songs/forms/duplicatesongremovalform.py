# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
"""
The duplicate song removal logic for OpenLP.
"""
import codecs
import logging
import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate, build_icon
from openlp.core.lib.db import Manager
from openlp.core.lib.ui import UiStrings, critical_error_message_box
from openlp.core.ui.wizard import OpenLPWizard, WizardStrings
from openlp.core.utils import AppLocation
from openlp.plugins.songs.lib.db import Song, MediaFile
from openlp.plugins.songs.lib.xml import SongXML
from openlp.plugins.songs.lib.duplicatesongfinder import DuplicateSongFinder

log = logging.getLogger(__name__)

class DuplicateSongRemovalForm(OpenLPWizard):
    """
    This is the Duplicate Song Removal Wizard. It provides functionality to
    search for and remove duplicate songs in the database.
    """
    log.info(u'DuplicateSongRemovalForm loaded')

    def __init__(self, parent, plugin):
        """
        Instantiate the wizard, and run any extra setup we need to.

        ``parent``
            The QWidget-derived parent of the wizard.

        ``plugin``
            The songs plugin.
        """
        self.duplicateSongList = []
        self.reviewCurrentCount = 0
        self.reviewTotalCount = 0
        self.clipboard = plugin.formParent.clipboard
        OpenLPWizard.__init__(self, parent, plugin, u'duplicateSongRemovalWizard',
            u':/wizards/wizard_duplicateremoval.bmp', False)

    def customInit(self):
        """
        Song wizard specific initialisation.
        """
        pass

    def customSignals(self):
        """
        Song wizard specific signals.
        """
        QtCore.QObject.connect(self.finishButton, QtCore.SIGNAL(u'clicked()'), self.onWizardExit)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(u'clicked()'), self.onWizardExit)

    def addCustomPages(self):
        """
        Add song wizard specific pages.
        """
        #add custom pages
        self.searchingPage = QtGui.QWizardPage()
        self.searchingPage.setObjectName('searchingPage')
        self.searchingVerticalLayout = QtGui.QVBoxLayout(self.searchingPage)
        self.searchingVerticalLayout.setObjectName('searchingVerticalLayout')
        self.duplicateSearchProgressBar = QtGui.QProgressBar(self.searchingPage)
        self.duplicateSearchProgressBar.setObjectName(u'duplicateSearchProgressBar')
        self.duplicateSearchProgressBar.setFormat(WizardStrings.PercentSymbolFormat)
        self.searchingVerticalLayout.addWidget(self.duplicateSearchProgressBar)
        self.foundDuplicatesEdit = QtGui.QPlainTextEdit(self.searchingPage)
        self.foundDuplicatesEdit.setUndoRedoEnabled(False)
        self.foundDuplicatesEdit.setReadOnly(True)
        self.foundDuplicatesEdit.setObjectName('foundDuplicatesEdit')
        self.searchingVerticalLayout.addWidget(self.foundDuplicatesEdit)
        self.searchingPageId = self.addPage(self.searchingPage)
        self.reviewPage = QtGui.QWizardPage()
        self.reviewPage.setObjectName('reviewPage')
        self.headerVerticalLayout = QtGui.QVBoxLayout(self.reviewPage)
        self.headerVerticalLayout.setObjectName('headerVerticalLayout')
        self.reviewCounterLabel = QtGui.QLabel(self.reviewPage)
        self.reviewCounterLabel.setObjectName('reviewCounterLabel')
        self.headerVerticalLayout.addWidget(self.reviewCounterLabel)
        self.songsHorizontalScrollArea = QtGui.QScrollArea(self.reviewPage)
        self.songsHorizontalScrollArea.setObjectName('songsHorizontalScrollArea')
        self.songsHorizontalScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.songsHorizontalScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.songsHorizontalScrollArea.setFrameStyle(QtGui.QFrame.NoFrame)
        self.songsHorizontalScrollArea.setWidgetResizable(True)
        self.songsHorizontalScrollArea.setStyleSheet("QScrollArea#songsHorizontalScrollArea {background-color:transparent;}");
        self.songsHorizontalSongsWidget = QtGui.QWidget(self.songsHorizontalScrollArea)
        self.songsHorizontalSongsWidget.setObjectName('songsHorizontalSongsWidget')
        self.songsHorizontalSongsWidget.setStyleSheet("QWidget#songsHorizontalSongsWidget {background-color:transparent;}");
        self.songsHorizontalLayout = QtGui.QHBoxLayout(self.songsHorizontalSongsWidget)
        self.songsHorizontalLayout.setObjectName('songsHorizontalLayout')
        self.songsHorizontalLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.songsHorizontalScrollArea.setWidget(self.songsHorizontalSongsWidget)
        self.headerVerticalLayout.addWidget(self.songsHorizontalScrollArea)
        self.reviewPageId = self.addPage(self.reviewPage)
        #add a dummy page to the end, to prevent the finish button to appear and the next button do disappear on the
        #review page
        self.dummyPage = QtGui.QWizardPage()
        self.dummyPageId = self.addPage(self.dummyPage)

    def retranslateUi(self):
        """
        Song wizard localisation.
        """
        self.setWindowTitle(translate('Wizard', 'Wizard'))
        self.titleLabel.setText(WizardStrings.HeaderStyle % translate('OpenLP.Ui',
            'Welcome to the Duplicate Song Removal Wizard'))
        self.informationLabel.setText(translate("Wizard",
            'This wizard will help you to remove duplicate songs from the song database.'))
        self.searchingPage.setTitle(translate('Wizard', 'Searching for doubles'))
        self.searchingPage.setSubTitle(translate('Wizard', 'The song database is searched for double songs.'))
        self.updateReviewCounterText()
        self.reviewPage.setSubTitle(translate('Wizard',
            'This page shows all duplicate songs to review which ones to remove and which ones to keep.'))

    def updateReviewCounterText(self):
        self.reviewPage.setTitle(translate('Wizard', 'Review duplicate songs (%s/%s)') % \
                (self.reviewCurrentCount, self.reviewTotalCount))

    def customPageChanged(self, pageId):
        """
        Called when changing to a page other than the progress page.
        """
        #hide back button
        self.button(QtGui.QWizard.BackButton).hide()
        if pageId == self.searchingPageId:
            #search duplicate songs
            maxSongs = self.plugin.manager.get_object_count(Song)
            if maxSongs == 0 or maxSongs == 1:
                return
            # with x songs we have x*(x-1)/2 comparisons
            maxProgressCount = maxSongs*(maxSongs-1)/2
            self.duplicateSearchProgressBar.setMaximum(maxProgressCount)
            songs = self.plugin.manager.get_all_objects(Song)
            for outerSongCounter in range(maxSongs-1):
                for innerSongCounter in range(outerSongCounter+1, maxSongs):
                    doubleFinder = DuplicateSongFinder()
                    if doubleFinder.songsProbablyEqual(songs[outerSongCounter], songs[innerSongCounter]):
                        self.addDuplicatesToSongList(songs[outerSongCounter], songs[innerSongCounter])
                        self.foundDuplicatesEdit.appendPlainText(songs[outerSongCounter].title + "  =  " + songs[innerSongCounter].title)
                    self.duplicateSearchProgressBar.setValue(self.duplicateSearchProgressBar.value()+1)
            self.reviewTotalCount = len(self.duplicateSongList)
            if self.reviewTotalCount == 0:
                self.button(QtGui.QWizard.FinishButton).show()
                self.button(QtGui.QWizard.FinishButton).setEnabled(True)
                self.button(QtGui.QWizard.NextButton).hide()
                QtGui.QMessageBox.information(self, translate('Wizard', 'Information'),
                    translate('Wizard', 'No duplicate songs have been found in the database.'),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
        elif pageId == self.reviewPageId:
            self.nextReviewButtonClicked()

    def addDuplicatesToSongList(self, searchSong, duplicateSong):
        duplicateGroupFound = False
        for duplicates in self.duplicateSongList:
            #skip the first song in the duplicate lists, since the first one has to be an earlier song
            for duplicate in duplicates[1:]:
                if duplicate == searchSong:
                    duplicates.append(duplicateSong)
                    duplicateGroupFound = True
                    break
                elif duplicate == duplicateSong:
                    duplicates.append(searchSong)
                    duplicateGroupFound = True
                    break
            if duplicateGroupFound:
                break
        if not duplicateGroupFound:
            self.duplicateSongList.append([searchSong, duplicateSong])

    def onWizardExit(self):
        #refresh the song list
        self.plugin.mediaItem.onSearchTextButtonClicked()
        pass

    def setDefaults(self):
        """
        Set default form values for the song import wizard.
        """
        self.restart()
        self.duplicateSearchProgressBar.setValue(0)
        self.foundDuplicatesEdit.clear()

    def performWizard(self):
        """
        Perform the actual import. This method pulls in the correct importer
        class, and then runs the ``doImport`` method of the importer to do
        the actual importing.
        """
        pass

    def validateCurrentPage(self):
        if self.currentId() == self.reviewPageId:
            #as long as the duplicate list is not empty we revisit the review page
            if len(self.duplicateSongList) == 0:
                return True
            else:
                self.nextReviewButtonClicked()
                return False
        return OpenLPWizard.validateCurrentPage(self)

    def removeButtonClicked(self, songReviewWidget):
        #remove song
        item_id = songReviewWidget.song.id
        media_files = self.plugin.manager.get_all_objects(MediaFile,
            MediaFile.song_id == item_id)
        for media_file in media_files:
            try:
                os.remove(media_file.file_name)
            except:
                log.exception('Could not remove file: %s',
                    media_file.file_name)
        try:
            save_path = os.path.join(AppLocation.get_section_data_path(
                self.plugin.name), 'audio', str(item_id))
            if os.path.exists(save_path):
                os.rmdir(save_path)
        except OSError:
            log.exception(u'Could not remove directory: %s', save_path)
        self.plugin.manager.delete_object(Song, item_id)
        # remove GUI elements
        self.songsHorizontalLayout.removeWidget(songReviewWidget)
        songReviewWidget.setParent(None)
        # check if we only have one SongReviewWidget left
        # 4 stretches + 1 SongReviewWidget = 5
        # the SongReviewWidget is then at position 2
        if self.songsHorizontalLayout.count() == 5:
            self.songsHorizontalLayout.itemAt(2).widget().songRemoveButton.setEnabled(False)

    def nextReviewButtonClicked(self):
        # update counter
        self.reviewCurrentCount = self.reviewTotalCount - (len(self.duplicateSongList) - 1)
        self.updateReviewCounterText()
        # remove all previous elements
        for i in reversed(range(self.songsHorizontalLayout.count())): 
            item = self.songsHorizontalLayout.itemAt(i)
            if isinstance(item, QtGui.QWidgetItem):
                # the order is important here, if the .setParent(None) call is done before the .removeItem() call, a
                # segfault occurs
                widget = item.widget()
                self.songsHorizontalLayout.removeItem(item) 
                widget.setParent(None)
            else:
                self.songsHorizontalLayout.removeItem(item) 
        #add next set of duplicates
        if len(self.duplicateSongList) > 0:
            # a stretch doesn't seem to stretch endlessly, so I add two to get enough stetch for 1400x1050
            self.songsHorizontalLayout.addStretch()
            self.songsHorizontalLayout.addStretch()
            for duplicate in self.duplicateSongList.pop(0):
                songReviewWidget = SongReviewWidget(self.reviewPage, duplicate)
                QtCore.QObject.connect(songReviewWidget,
                        QtCore.SIGNAL(u'songRemoveButtonClicked(PyQt_PyObject)'),
                        self.removeButtonClicked)
                self.songsHorizontalLayout.addWidget(songReviewWidget)
            self.songsHorizontalLayout.addStretch()
            self.songsHorizontalLayout.addStretch()
        #change next button to finish button on last review
        if len(self.duplicateSongList) == 0:
            self.button(QtGui.QWizard.FinishButton).show()
            self.button(QtGui.QWizard.FinishButton).setEnabled(True)
            self.button(QtGui.QWizard.NextButton).hide()

class SongReviewWidget(QtGui.QWidget):
    def __init__(self, parent, song):
        QtGui.QWidget.__init__(self, parent)
        self.song = song
        self.setupUi()
        self.retranslateUi()
        QtCore.QObject.connect(self.songRemoveButton, QtCore.SIGNAL(u'clicked()'), self.onRemoveButtonClicked)

    def setupUi(self):
        self.songVerticalLayout = QtGui.QVBoxLayout(self)
        self.songVerticalLayout.setObjectName(u'songVerticalLayout')
        self.songGroupBox = QtGui.QGroupBox(self)
        self.songGroupBox.setObjectName(u'songGroupBox')
        self.songGroupBox.setMinimumWidth(300)
        self.songGroupBox.setMaximumWidth(300)
        self.songGroupBoxLayout = QtGui.QVBoxLayout(self.songGroupBox)
        self.songGroupBoxLayout.setObjectName(u'songGroupBoxLayout')
        self.songScrollArea = QtGui.QScrollArea(self)
        self.songScrollArea.setObjectName(u'songScrollArea')
        self.songScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.songScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.songScrollArea.setFrameStyle(QtGui.QFrame.NoFrame)
        self.songScrollArea.setWidgetResizable(True)
        self.songContentWidget = QtGui.QWidget(self.songScrollArea)
        self.songContentWidget.setObjectName(u'songContentWidget')
        self.songContentVerticalLayout = QtGui.QVBoxLayout(self.songContentWidget)
        self.songContentVerticalLayout.setObjectName(u'songContentVerticalLayout')
        self.songContentVerticalLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.songInfoFormLayout = QtGui.QFormLayout()
        self.songInfoFormLayout.setObjectName(u'songInfoFormLayout')
        self.songTitleLabel = QtGui.QLabel(self)
        self.songTitleLabel.setObjectName(u'songTitleLabel')
        self.songInfoFormLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.songTitleLabel)
        self.songTitleContent = QtGui.QLabel(self)
        self.songTitleContent.setObjectName(u'songTitleContent')
        self.songTitleContent.setText(self.song.title)
        self.songTitleContent.setWordWrap(True)
        self.songInfoFormLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.songTitleContent)
        self.songAlternateTitleLabel = QtGui.QLabel(self)
        self.songAlternateTitleLabel.setObjectName(u'songAlternateTitleLabel')
        self.songInfoFormLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.songAlternateTitleLabel)
        self.songAlternateTitleContent = QtGui.QLabel(self)
        self.songAlternateTitleContent.setObjectName(u'songAlternateTitleContent')
        self.songAlternateTitleContent.setText(self.song.alternate_title)
        self.songAlternateTitleContent.setWordWrap(True)
        self.songInfoFormLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.songAlternateTitleContent)
        self.songCCLINumberLabel = QtGui.QLabel(self)
        self.songCCLINumberLabel.setObjectName(u'songCCLINumberLabel')
        self.songInfoFormLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.songCCLINumberLabel)
        self.songCCLINumberContent = QtGui.QLabel(self)
        self.songCCLINumberContent.setObjectName(u'songCCLINumberContent')
        self.songCCLINumberContent.setText(self.song.ccli_number)
        self.songCCLINumberContent.setWordWrap(True)
        self.songInfoFormLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.songCCLINumberContent)
        self.songCopyrightLabel = QtGui.QLabel(self)
        self.songCopyrightLabel.setObjectName(u'songCopyrightLabel')
        self.songInfoFormLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.songCopyrightLabel)
        self.songCopyrightContent = QtGui.QLabel(self)
        self.songCopyrightContent.setObjectName(u'songCopyrightContent')
        self.songCopyrightContent.setWordWrap(True)
        self.songCopyrightContent.setText(self.song.copyright)
        self.songInfoFormLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.songCopyrightContent)
        self.songCommentsLabel = QtGui.QLabel(self)
        self.songCommentsLabel.setObjectName(u'songCommentsLabel')
        self.songInfoFormLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.songCommentsLabel)
        self.songCommentsContent = QtGui.QLabel(self)
        self.songCommentsContent.setObjectName(u'songCommentsContent')
        self.songCommentsContent.setText(self.song.comments)
        self.songCommentsContent.setWordWrap(True)
        self.songInfoFormLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.songCommentsContent)
        self.songAuthorsLabel = QtGui.QLabel(self)
        self.songAuthorsLabel.setObjectName(u'songAuthorsLabel')
        self.songInfoFormLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.songAuthorsLabel)
        self.songAuthorsContent = QtGui.QLabel(self)
        self.songAuthorsContent.setObjectName(u'songAuthorsContent')
        self.songAuthorsContent.setWordWrap(True)
        authorsText = u''
        for author in self.song.authors:
            authorsText += author.display_name + ', '
        if authorsText:
            authorsText = authorsText[:-2]
        self.songAuthorsContent.setText(authorsText)
        self.songInfoFormLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.songAuthorsContent)
        self.songVerseOrderLabel = QtGui.QLabel(self)
        self.songVerseOrderLabel.setObjectName(u'songVerseOrderLabel')
        self.songInfoFormLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.songVerseOrderLabel)
        self.songVerseOrderContent = QtGui.QLabel(self)
        self.songVerseOrderContent.setObjectName(u'songVerseOrderContent')
        self.songVerseOrderContent.setText(self.song.verse_order)
        self.songVerseOrderContent.setWordWrap(True)
        self.songInfoFormLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.songVerseOrderContent)
        self.songContentVerticalLayout.addLayout(self.songInfoFormLayout)
        self.songInfoVerseGroupBox = QtGui.QGroupBox(self.songGroupBox)
        self.songInfoVerseGroupBox.setObjectName(u'songInfoVerseGroupBox')
        self.songInfoVerseGroupBoxLayout = QtGui.QFormLayout(self.songInfoVerseGroupBox)
        songXml = SongXML()
        verses = songXml.get_verses(self.song.lyrics)
        for verse in verses:
            verseMarker = verse[0]['type'] + verse[0]['label']
            verseLabel = QtGui.QLabel(self.songInfoVerseGroupBox)
            verseLabel.setText(verse[1])
            verseLabel.setWordWrap(True)
            self.songInfoVerseGroupBoxLayout.addRow(verseMarker, verseLabel)
        self.songContentVerticalLayout.addWidget(self.songInfoVerseGroupBox)
        self.songContentVerticalLayout.addStretch()
        self.songScrollArea.setWidget(self.songContentWidget)
        self.songGroupBoxLayout.addWidget(self.songScrollArea)
        self.songVerticalLayout.addWidget(self.songGroupBox)
        self.songRemoveButton = QtGui.QPushButton(self)
        self.songRemoveButton.setObjectName(u'songRemoveButton')
        self.songRemoveButton.setIcon(build_icon(u':/songs/song_delete.png'))
        self.songRemoveButton.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.songVerticalLayout.addWidget(self.songRemoveButton, alignment = QtCore.Qt.AlignHCenter)

    def retranslateUi(self):
        self.songRemoveButton.setText(u'Remove')
        self.songTitleLabel.setText(u'Title:')
        self.songAlternateTitleLabel.setText(u'Alternate Title:')
        self.songCCLINumberLabel.setText(u'CCLI Number:')
        self.songVerseOrderLabel.setText(u'Verse Order:')
        self.songCopyrightLabel.setText(u'Copyright:')
        self.songCommentsLabel.setText(u'Comments:')
        self.songAuthorsLabel.setText(u'Authors:')
        self.songInfoVerseGroupBox.setTitle(u'Verses')

    def onRemoveButtonClicked(self):
        self.emit(QtCore.SIGNAL(u'songRemoveButtonClicked(PyQt_PyObject)'), self)

