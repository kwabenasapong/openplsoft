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
This module contains tests for the SongShow Plus song importer.
"""

import os
from unittest import TestCase

from tests.helpers.songfileimport import SongImportTestHelper
from openlp.plugins.songs.lib import VerseType
from openlp.plugins.songs.lib.songshowplusimport import SongShowPlusImport
from tests.functional import patch, MagicMock

TEST_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources', 'songshowplussongs'))

class TestSongShowPlusFileImport(SongImportTestHelper):
    def __init__(self, *args, **kwargs):
        self.importer_class_name = 'SongShowPlusImport'
        self.importer_module_name = 'songshowplusimport'
        super(TestSongShowPlusFileImport, self).__init__(*args, **kwargs)

    def test_song_import(self):
        test_import = self.file_import(os.path.join(TEST_PATH, 'Amazing Grace.sbsong'),
            self.load_external_result_data(os.path.join(TEST_PATH, 'Amazing Grace.json')))
        test_import = self.file_import(os.path.join(TEST_PATH, 'Beautiful Garden Of Prayer.sbsong'),
            self.load_external_result_data(os.path.join(TEST_PATH, 'Beautiful Garden Of Prayer.json')))


class TestSongShowPlusImport(TestCase):
    """
    Test the functions in the :mod:`songshowplusimport` module.
    """
    def create_importer_test(self):
        """
        Test creating an instance of the SongShow Plus file importer
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch('openlp.plugins.songs.lib.songshowplusimport.SongImport'):
            mocked_manager = MagicMock()

            # WHEN: An importer object is created
            importer = SongShowPlusImport(mocked_manager)

            # THEN: The importer object should not be None
            self.assertIsNotNone(importer, 'Import should not be none')

    def invalid_import_source_test(self):
        """
        Test SongShowPlusImport.doImport handles different invalid import_source values
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch('openlp.plugins.songs.lib.songshowplusimport.SongImport'):
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            importer = SongShowPlusImport(mocked_manager)
            importer.import_wizard = mocked_import_wizard
            importer.stop_import_flag = True

            # WHEN: Import source is not a list
            for source in ['not a list', 0]:
                importer.import_source = source

                # THEN: doImport should return none and the progress bar maximum should not be set.
                self.assertIsNone(importer.doImport(), 'doImport should return None when import_source is not a list')
                self.assertEquals(mocked_import_wizard.progress_bar.setMaximum.called, False,
                                  'setMaximum on import_wizard.progress_bar should not have been called')

    def valid_import_source_test(self):
        """
        Test SongShowPlusImport.doImport handles different invalid import_source values
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch('openlp.plugins.songs.lib.songshowplusimport.SongImport'):
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            importer = SongShowPlusImport(mocked_manager)
            importer.import_wizard = mocked_import_wizard
            importer.stop_import_flag = True

            # WHEN: Import source is a list
            importer.import_source = ['List', 'of', 'files']

            # THEN: doImport should return none and the progress bar setMaximum should be called with the length of
            #       import_source.
            self.assertIsNone(importer.doImport(),
                'doImport should return None when import_source is a list and stop_import_flag is True')
            mocked_import_wizard.progress_bar.setMaximum.assert_called_with(len(importer.import_source))

    def to_openlp_verse_tag_test(self):
        """
        Test to_openlp_verse_tag method by simulating adding a verse
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch('openlp.plugins.songs.lib.songshowplusimport.SongImport'):
            mocked_manager = MagicMock()
            importer = SongShowPlusImport(mocked_manager)

            # WHEN: Supplied with the following arguments replicating verses being added
            test_values = [('Verse 1', VerseType.tags[VerseType.Verse] + '1'),
                ('Verse 2', VerseType.tags[VerseType.Verse] + '2'),
                ('verse1', VerseType.tags[VerseType.Verse] + '1'),
                ('Verse', VerseType.tags[VerseType.Verse] + '1'),
                ('Verse1', VerseType.tags[VerseType.Verse] + '1'),
                ('chorus 1', VerseType.tags[VerseType.Chorus] + '1'),
                ('bridge 1', VerseType.tags[VerseType.Bridge] + '1'),
                ('pre-chorus 1', VerseType.tags[VerseType.PreChorus] + '1'),
                ('different 1', VerseType.tags[VerseType.Other] + '1'),
                ('random 1', VerseType.tags[VerseType.Other] + '2')]

            # THEN: The returned value should should correlate with the input arguments
            for original_tag, openlp_tag in test_values:
                self.assertEquals(importer.to_openlp_verse_tag(original_tag), openlp_tag,
                    'SongShowPlusImport.to_openlp_verse_tag should return "%s" when called with "%s"'
                    % (openlp_tag, original_tag))

    def to_openlp_verse_tag_verse_order_test(self):
        """
        Test to_openlp_verse_tag method by simulating adding a verse to the verse order
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch('openlp.plugins.songs.lib.songshowplusimport.SongImport'):
            mocked_manager = MagicMock()
            importer = SongShowPlusImport(mocked_manager)

            # WHEN: Supplied with the following arguments replicating a verse order being added
            test_values = [('Verse 1', VerseType.tags[VerseType.Verse] + '1'),
                ('Verse 2', VerseType.tags[VerseType.Verse] + '2'),
                ('verse1', VerseType.tags[VerseType.Verse] + '1'),
                ('Verse', VerseType.tags[VerseType.Verse] + '1'),
                ('Verse1', VerseType.tags[VerseType.Verse] + '1'),
                ('chorus 1', VerseType.tags[VerseType.Chorus] + '1'),
                ('bridge 1', VerseType.tags[VerseType.Bridge] + '1'),
                ('pre-chorus 1', VerseType.tags[VerseType.PreChorus] + '1'),
                ('different 1', VerseType.tags[VerseType.Other] + '1'),
                ('random 1', VerseType.tags[VerseType.Other] + '2'),
                ('unused 2', None)]

            # THEN: The returned value should should correlate with the input arguments
            for original_tag, openlp_tag in test_values:
                self.assertEquals(importer.to_openlp_verse_tag(original_tag, ignore_unique=True), openlp_tag,
                    'SongShowPlusImport.to_openlp_verse_tag should return "%s" when called with "%s"'
                    % (openlp_tag, original_tag))