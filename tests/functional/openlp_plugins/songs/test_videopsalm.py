# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2019 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
"""
This module contains tests for the VideoPsalm song importer.
"""
from unittest.mock import MagicMock, patch

from tests.helpers.songfileimport import SongImportTestHelper
from tests.utils.constants import RESOURCE_PATH


TEST_PATH = RESOURCE_PATH / 'songs' / 'videopsalm'


class TestVideoPsalmFileImport(SongImportTestHelper):

    def __init__(self, *args, **kwargs):
        self.importer_class_name = 'VideoPsalmImport'
        self.importer_module_name = 'videopsalm'
        super(TestVideoPsalmFileImport, self).__init__(*args, **kwargs)

    @patch('openlp.plugins.songs.lib.importers.videopsalm.Settings')
    def test_song_import(self, mocked_settings):
        """
        Test that loading an VideoPsalm file works correctly on various files
        """
        # Mock out the settings - always return False
        mocked_returned_settings = MagicMock()
        mocked_returned_settings.value.side_effect = lambda value: True if value == 'songs/enable chords' else False
        mocked_settings.return_value = mocked_returned_settings
        # Do the test import
        self.file_import(TEST_PATH / 'videopsalm-as-safe-a-stronghold.json',
                         self.load_external_result_data(TEST_PATH / 'as-safe-a-stronghold.json'))
        self.file_import(TEST_PATH / 'videopsalm-as-safe-a-stronghold2.json',
                         self.load_external_result_data(TEST_PATH / 'as-safe-a-stronghold2.json'))
