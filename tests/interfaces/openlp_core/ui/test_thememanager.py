# -*- coding: utf-8 -*-

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
Interface tests to test the themeManager class and related methods.
"""
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

from openlp.core.common.registry import Registry
from openlp.core.common.settings import Settings
from openlp.core.ui.thememanager import ThemeManager
from tests.helpers.testmixin import TestMixin


class TestThemeManager(TestCase, TestMixin):
    """
    Test the functions in the ThemeManager module
    """
    def setUp(self):
        """
        Create the UI
        """
        self.setup_application()
        self.build_settings()
        Registry.create()
        self.theme_manager = ThemeManager()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        self.destroy_settings()
        del self.theme_manager

    def test_initialise(self):
        """
        Test the thememanager initialise - basic test
        """
        # GIVEN: A new a call to initialise
        self.theme_manager.setup_ui = MagicMock()
        self.theme_manager.build_theme_path = MagicMock()
        Settings().setValue('themes/global theme', 'my_theme')

        # WHEN: the initialisation is run
        self.theme_manager.bootstrap_initialise()

        # THEN:
        self.theme_manager.setup_ui.assert_called_once_with(self.theme_manager)
        assert self.theme_manager.global_theme == 'my_theme'
        self.theme_manager.build_theme_path.assert_called_once_with()

    @patch('openlp.core.ui.thememanager.create_paths')
    @patch('openlp.core.ui.thememanager.AppLocation.get_section_data_path')
    def test_build_theme_path(self, mocked_get_section_data_path, mocked_create_paths):
        """
        Test the thememanager build_theme_path
        """
        # GIVEN: A mocked out AppLocation.get_directory() and mocked create_paths
        mocked_get_section_data_path.return_value = Path('tests/my_theme')

        # WHEN: the build_theme_path is run
        self.theme_manager.build_theme_path()

        #  THEN: The theme path and the thumb path should be correct
        assert self.theme_manager.theme_path == Path('tests/my_theme')
        assert self.theme_manager.thumb_path == Path('tests/my_theme/thumbnails')
        mocked_create_paths.assert_called_once_with(Path('tests/my_theme'), Path('tests/my_theme/thumbnails'))

    def test_click_on_new_theme(self):
        """
        Test the on_add_theme event handler is called by the UI
        """
        # GIVEN: An initial form
        Settings().setValue('themes/global theme', 'my_theme')
        mocked_event = MagicMock()
        self.theme_manager.on_add_theme = mocked_event
        self.theme_manager.setup_ui(self.theme_manager)

        # WHEN displaying the UI and pressing cancel
        new_theme = self.theme_manager.toolbar.actions['newTheme']
        new_theme.trigger()

        assert mocked_event.call_count == 1, 'The on_add_theme method should have been called once'

    @patch('openlp.core.ui.themeform.ThemeForm._setup')
    @patch('openlp.core.ui.filerenameform.FileRenameForm._setup')
    def test_bootstrap_post(self, mocked_rename_form, mocked_theme_form):
        """
        Test the functions of bootstrap_post_setup are called.
        """
        # GIVEN:
        self.theme_manager.theme_path = MagicMock()

        # WHEN:
        with patch('openlp.core.ui.thememanager.ThemeProgressForm'):
            self.theme_manager.bootstrap_post_set_up()

        # THEN:
        assert self.theme_manager.progress_form is not None
        assert self.theme_manager.theme_form is not None
        assert self.theme_manager.file_rename_form is not None

    def test_bootstrap_completion(self):
        """
        Test the functions of bootstrap_post_setup are called.
        """
        # GIVEN:
        self.theme_manager.load_themes = MagicMock()
        self.theme_manager.upgrade_themes = MagicMock()

        # WHEN:
        self.theme_manager.bootstrap_completion()

        # THEN:
        self.theme_manager.upgrade_themes.assert_called_once()
        self.theme_manager.load_themes.assert_called_once()
