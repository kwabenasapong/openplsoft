# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2022 OpenLP Developers                              #
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
This module contains tests for the OpenLyrics song importer.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from lxml import etree

from openlp.core.common.registry import Registry
from openlp.core.common.settings import Settings
from openlp.plugins.songs.lib.importers.openlyrics import OpenLyricsImport
from openlp.plugins.songs.lib.importers.songimport import SongImport
from openlp.plugins.songs.lib.ui import SongStrings
from tests.helpers.testmixin import TestMixin
from tests.utils.constants import RESOURCE_PATH


TEST_PATH = RESOURCE_PATH / 'songs' / 'openlyrics'
SONG_TEST_DATA = {
    'What a friend we have in Jesus.xml': {
        'title': 'What A Friend We Have In Jesus',
        'verses': [
            ('What a friend we have in Jesus, All ours sins and griefs to bear;\n\
             What a privilege to carry, Everything to God in prayer!\n\
             O what peace we often forfeit, O what needless pain we bear;\n\
             All because we do not carry, Everything to God in prayer!', 'v1'),
            ('Have we trials and temptations? Is there trouble anywhere?\n\
             We should never be discouraged, Take it to the Lord in prayer.\n\
             Can we find a friend so faithful? Who will all our sorrows share?\n\
             Jesus knows our every weakness; Take it to the Lord in prayer.', 'v2'),
            ('Are we weak and heavy laden, Cumbered with a load of care?\n\
             Precious Saviour still our refuge; Take it to the Lord in prayer.\n\
             Do thy friends despise forsake thee? Take it to the Lord in prayer!\n\
             In His arms He???ll take and shield thee; Thou wilt find a solace there.', 'v3')
        ]
    }
}


class TestOpenLyricsImport(TestCase, TestMixin):
    """
    Test the functions in the :mod:`openlyricsimport` module.
    """
    def setUp(self):
        """
        Create the registry
        """
        self.setup_application()
        Registry.create()
        self.build_settings()
        Registry().register('settings', Settings())

    def tearDown(self):
        """
        Cleanup
        """
        self.destroy_settings()

    def test_create_importer(self):
        """
        Test creating an instance of the OpenLyrics file importer
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch('openlp.plugins.songs.lib.importers.openlyrics.SongImport'):
            mocked_manager = MagicMock()

            # WHEN: An importer object is created
            importer = OpenLyricsImport(mocked_manager, file_paths=[])

            # THEN: The importer should be an instance of SongImport
            assert isinstance(importer, SongImport)

    def test_file_import(self):
        """
        Test the actual import of real song files
        """
        # GIVEN: Test files with a mocked out "manager" and a mocked out "import_wizard"
        for song_file in SONG_TEST_DATA:
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            importer = OpenLyricsImport(mocked_manager, file_paths=[])
            importer.import_wizard = mocked_import_wizard
            importer.open_lyrics = MagicMock()
            importer.open_lyrics.xml_to_song = MagicMock()

            # WHEN: Importing each file
            importer.import_source = [TEST_PATH / song_file]
            importer.do_import()

            # THEN: The xml_to_song() method should have been called
            assert importer.open_lyrics.xml_to_song.called is True

    def test_can_parse_file_having_a_processing_instruction(self):
        """
        Test files having a processing instruction can be parsed
        """
        # GIVEN: A OpenLyrics XML containing a processing instruction, an OpenLyrics importer with a mocked out
        # manager, import wizard and 'log_error' method, and a mocked out logger
        with patch('openlp.plugins.songs.lib.importers.openlyrics.log', autospec=True) as mocked_logger:
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            importer = OpenLyricsImport(mocked_manager, file_paths=[])
            importer.import_wizard = mocked_import_wizard
            importer.log_error = MagicMock()

            # WHEN: Importing a file which contains a processing instruction
            importer.import_source = [TEST_PATH / 'Amazing Grace.xml']
            try:
                importer.do_import()
            except Exception as ex:
                # THEN: no uncaught exception escaped from importer.do_import() is etree.XMLSyntaxError
                assert ex is not etree.XMLSyntaxError
                # otherwise we don't care about it now (but should in other tests...)
                pass

            # THEN: the importer's log_error method was never called with SongStrings.XMLSyntaxError as its second
            # positional argument
            if importer.log_error.called:
                for call_args in importer.log_error.call_args_list:
                    args = call_args[0]
                    # there are at least two positional arguments
                    if len(args) > 1:
                        assert args[1] is not SongStrings.XMLSyntaxError

            # THEN: the logger's 'exception' method was never called with a first positional argument
            # which is a string and starts with 'XML syntax error in file'
            if mocked_logger.exception.called:
                for call_args in mocked_logger.exception.call_args_list:
                    args = call_args[0]
                    # there is at least one positional argument and it is a string
                    if args and isinstance(args[0], str):
                        error_message = args[0]
                        assert not error_message.startswith('XML syntax error in file')

    def test_leading_and_trailing_whitespaces_inside_lines_tags_are_removed(self):
        """
        Test that leading and trailing whitespace inside <lines> tags and its descendants are removed
        """
        # GIVEN: One OpenLyrics XML with extra whitespaces in <lines> tag (Amazing_Grace_1.xml)
        # and a copy which only difference is that it lacks those whitespaces (Amazing_Grace_2.xml)
        mocked_manager = MagicMock()
        mocked_import_wizard = MagicMock()
        importer = OpenLyricsImport(mocked_manager, file_paths=[])
        importer.import_wizard = mocked_import_wizard
        importer.open_lyrics = MagicMock()
        importer.open_lyrics.xml_to_song = MagicMock()

        # WHEN: Importing the file not having those whitespaces...
        importer.import_source = [TEST_PATH / 'Amazing_Grace_2.xml']
        importer.do_import()

        # keep the parsed XML which is assumed to be the first positional argument of the xml_to_song() method
        importer.open_lyrics.xml_to_song.assert_called()
        no_whitespaces_xml = importer.open_lyrics.xml_to_song.call_args[0][0]

        # ... and importing the file having those whitespaces
        importer.import_source = [TEST_PATH / 'Amazing_Grace_1.xml']
        importer.do_import()

        # THEN: The last call of the xml_to_song() method should have got the same XML content as its first call
        importer.open_lyrics.xml_to_song.assert_called_with(no_whitespaces_xml)
