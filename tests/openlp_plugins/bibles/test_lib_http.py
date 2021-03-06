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
    Package to test the openlp.plugin.bible.lib.https package.
"""
import os
from unittest import TestCase, skipIf
from unittest.mock import MagicMock

from openlp.core.common.registry import Registry
from openlp.core.common.settings import Settings
from openlp.plugins.bibles.lib.importers.http import BGExtract, BSExtract, CWExtract

IS_CI = 'GITLAB_CI' in os.environ or 'APPVEYOR' in os.environ


@skipIf(IS_CI, 'Skip Bible HTTP tests to prevent GitLab CI from being blacklisted')
class TestBibleHTTP(TestCase):

    def setUp(self):
        """
        Set up the Registry
        """
        Registry.create()
        Registry().register('service_list', MagicMock())
        Registry().register('application', MagicMock())
        Registry().register('main_window', MagicMock())
        Registry().register('settings', Settings())

    def test_bible_gateway_extract_books(self):
        """
        Test the Bible Gateway retrieval of book list for NIV bible
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = BGExtract()

        # WHEN: The Books list is called
        books = handler.get_books_from_http('NIV')

        # THEN: We should get back a valid service item
        assert len(books) == 66, 'The bible should not have had any books added or removed'
        assert books[0] == 'Genesis', 'The first bible book should be Genesis'

    def test_bible_gateway_extract_books_support_redirect(self):
        """
        Test the Bible Gateway retrieval of book list for DN1933 bible with redirect (bug 1251437)
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = BGExtract()

        # WHEN: The Books list is called
        books = handler.get_books_from_http('DN1933')

        # THEN: We should get back a valid service item
        assert len(books) == 66, 'This bible should have 66 books'

    def test_bible_gateway_extract_verse(self):
        """
        Test the Bible Gateway retrieval of verse list for NIV bible John 3
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = BGExtract()

        # WHEN: The Books list is called
        results = handler.get_bible_chapter('NIV', 'John', 3)

        # THEN: We should get back a valid service item
        assert len(results.verse_list) == 36, 'The book of John should not have had any verses added or removed'

    def test_bible_gateway_extract_verse_nkjv(self):
        """
        Test the Bible Gateway retrieval of verse list for NKJV bible John 3
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = BGExtract()

        # WHEN: The Books list is called
        results = handler.get_bible_chapter('NKJV', 'John', 3)

        # THEN: We should get back a valid service item
        assert len(results.verse_list) == 36, 'The book of John should not have had any verses added or removed'

    def test_crosswalk_extract_books(self):
        """
        Test Crosswalk retrieval of book list for NIV bible
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = CWExtract()

        # WHEN: The Books list is called
        books = handler.get_books_from_http('niv')

        # THEN: We should get back a valid service item
        assert len(books) == 66, 'The bible should not have had any books added or removed'

    def test_crosswalk_extract_verse(self):
        """
        Test Crosswalk retrieval of verse list for NIV bible John 3
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = CWExtract()

        # WHEN: The Books list is called
        results = handler.get_bible_chapter('niv', 'john', 3)

        # THEN: We should get back a valid service item
        assert len(results.verse_list) == 36, 'The book of John should not have had any verses added or removed'

    def test_crosswalk_get_bibles(self):
        """
        Test getting list of bibles from Crosswalk.com
        """
        # GIVEN: A new Crosswalk extraction class
        handler = CWExtract()

        # WHEN: downloading bible list from Crosswalk
        bibles = handler.get_bibles_from_http()

        # THEN: The list should not be None, and some known bibles should be there
        assert bibles is not None
        assert ('Giovanni Diodati 1649 (Italian)', 'gdb', 'it') in bibles

    def test_crosswalk_get_verse_text(self):
        """
        Test verse text from Crosswalk.com
        """
        # GIVEN: A new Crosswalk extraction class
        handler = CWExtract()

        # WHEN: downloading NIV Genesis from Crosswalk
        niv_genesis_chapter_one = handler.get_bible_chapter('niv', 'Genesis', 1)

        # THEN: The verse list should contain the verses
        assert niv_genesis_chapter_one.has_verse_list() is True
        assert 'In the beginning God created the heavens and the earth.' == niv_genesis_chapter_one.verse_list[1], \
            'The first chapter of genesis should have been fetched.'

    def test_bibleserver_get_bibles(self):
        """
        Test getting list of bibles from BibleServer.com
        """
        # GIVEN: A new Bible Server extraction class
        handler = BSExtract()

        # WHEN: downloading bible list from bibleserver
        bibles = handler.get_bibles_from_http()

        # THEN: The list should not be None, and some known bibles should be there
        assert bibles is not None
        assert ('New Int. Readers Version', 'NIRV', 'en') in bibles
        assert ('?????????????????? ??????????????, ?????????????????? ??????????????', 'CARS', 'ru') in bibles

    def test_bibleserver_get_verse_text(self):
        """
        Test verse text from bibleserver.com
        """
        # GIVEN: A new Crosswalk extraction class
        handler = BSExtract()

        # WHEN: downloading NIV Genesis from Crosswalk
        niv_genesis_chapter_one = handler.get_bible_chapter('NIV', 'Genesis', 1)

        # THEN: The verse list should contain the verses
        assert niv_genesis_chapter_one.has_verse_list() is True
        assert 'In the beginning God created the heavens and the earth.' == niv_genesis_chapter_one.verse_list[1], \
            'The first chapter of genesis should have been fetched.'

    def test_biblegateway_get_bibles(self):
        """
        Test getting list of bibles from BibleGateway.com
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = BGExtract()

        # WHEN: downloading bible list from Crosswalk
        bibles = handler.get_bibles_from_http()

        # THEN: The list should not be None, and some known bibles should be there
        assert bibles is not None
        assert ('Holman Christian Standard Bible (HCSB)', 'HCSB', 'en') in bibles
