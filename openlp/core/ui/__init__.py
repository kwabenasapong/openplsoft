# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
The :mod:`ui` module provides the core user interface for OpenLP
"""
from PyQt4 import QtGui

from openlp.core.lib import translate, Receiver

class HideMode(object):
    """
    This is an enumeration class which specifies the different modes of hiding
    the display.

    ``Blank``
        This mode is used to hide all output, specifically by covering the
        display with a black screen.

    ``Theme``
        This mode is used to hide all output, but covers the display with the
        current theme background, as opposed to black.

    ``Desktop``
        This mode hides all output by minimising the display, leaving the user's
        desktop showing.
    """
    Blank = 1
    Theme = 2
    Screen = 3

from themeform import ThemeForm
from filerenameform import FileRenameForm
from maindisplay import MainDisplay
from servicenoteform import ServiceNoteForm
from serviceitemeditform import ServiceItemEditForm
from screen import ScreenList
from slidecontroller import SlideController
from splashscreen import SplashScreen
from generaltab import GeneralTab
from themestab import ThemesTab
from advancedtab import AdvancedTab
from displaytagtab import DisplayTagTab
from aboutform import AboutForm
from pluginform import PluginForm
from settingsform import SettingsForm
from shortcutlistform import ShortcutListForm
from mediadockmanager import MediaDockManager
from servicemanager import ServiceManager
from thememanager import ThemeManager

__all__ = ['SplashScreen', 'AboutForm', 'SettingsForm', 'MainDisplay',
    'SlideController', 'ServiceManager', 'ThemeManager', 'MediaDockManager',
    'ServiceItemEditForm',]
