# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
import os
import time
from subprocess import Popen

from openlp.core.common import is_macosx, Registry, delete_file

if is_macosx() and os.path.exists('/Applications/LibreOffice.app'):
    macuno_available = True
else:
    macuno_available = False

from PyQt5 import QtCore
from Pyro4 import Proxy

from openlp.core.lib import ScreenList
from .presentationcontroller import PresentationController, PresentationDocument, TextType


log = logging.getLogger(__name__)


class MacLOController(PresentationController):
    """
    Class to control interactions with MacLO presentations on Mac OS X via Pyro4. It starts the Pyro4 nameserver,
    starts the LibreOfficeServer, and then controls MacLO via Pyro4.
    """
    log.info('MacLOController loaded')

    def __init__(self, plugin):
        """
        Initialise the class
        """
        log.debug('Initialising')
        super(MacLOController, self).__init__(plugin, 'Impress on macOS', MacLODocument)
        self.supports = ['odp']
        self.also_supports = ['ppt', 'pps', 'pptx', 'ppsx', 'pptm']
        self.server_process = None
        self._client = None
        self._start_server()

    def _start_server(self):
        """
        Start a LibreOfficeServer
        """
        libreoffice_python = '/Applications/LibreOffice.app/Contents/Resources/python'
        libreoffice_server = os.path.join(os.path.dirname(__file__), 'libreofficeserver.py')
        self.server_process = Popen([libreoffice_python, libreoffice_server])

    @property
    def client(self):
        """
        Set up a Pyro4 client so that we can talk to the LibreOfficeServer
        """
        if not self._client:
            self._client = Proxy('PYRO:openlp.libreofficeserver@localhost:4310')
        if not self._client._pyroConnection:
            self._client._pyroReconnect()
        return self._client

    def check_available(self):
        """
        MacLO is able to run on this machine.
        """
        log.debug('check_available')
        return macuno_available

    def start_process(self):
        """
        Loads a running version of LibreOffice in the background. It is not displayed to the user but is available to
        the UNO interface when required.
        """
        log.debug('Started automatically by the Pyro server')
        self.client.start_process()

    def kill(self):
        """
        Called at system exit to clean up any running presentations.
        """
        log.debug('Kill LibreOffice')
        self.client.shutdown()
        self.server_process.kill()


class MacLODocument(PresentationDocument):
    """
    Class which holds information and controls a single presentation.
    """

    def __init__(self, controller, presentation):
        """
        Constructor, store information about the file and initialise.
        """
        log.debug('Init Presentation LibreOffice')
        super(MacLODocument, self).__init__(controller, presentation)
        self.client = controller.client

    def load_presentation(self):
        """
        Called when a presentation is added to the SlideController. It builds the environment, starts communcations with
        the background LibreOffice task started earlier. If LibreOffice is not present is is started. Once the environment
        is available the presentation is loaded and started.
        """
        log.debug('Load Presentation LibreOffice')
        self.client.setup_desktop()
        if not self.client.has_desktop():
            return False
        if not self.client.load_presentation(self.file_path, ScreenList().current['number'] + 1):
            return False
        self.create_thumbnails()
        self.create_titles_and_notes()
        return True

    def create_thumbnails(self):
        """
        Create thumbnail images for presentation.
        """
        log.debug('create thumbnails LibreOffice')
        if self.check_thumbnails():
            return
        temp_thumbnails = self.client.extract_thumbnails(self.get_temp_folder())
        for index, temp_thumb in enumerate(temp_thumbnails):
            self.convert_thumbnail(temp_thumb, index + 1)
            delete_file(temp_thumb)

    def create_titles_and_notes(self):
        """
        Writes the list of titles (one per slide) to 'titles.txt' and the notes to 'slideNotes[x].txt'
        in the thumbnails directory
        """
        titles, notes = self.client.get_titles_and_notes()
        self.save_titles_and_notes(titles, notes)

    def close_presentation(self):
        """
        Close presentation and clean up objects. Triggered by new object being added to SlideController or OpenLP being
        shutdown.
        """
        log.debug('close Presentation LibreOffice')
        self.client.close_presentation()
        self.controller.remove_doc(self)

    def is_loaded(self):
        """
        Returns true if a presentation is loaded.
        """
        log.debug('is loaded LibreOffice')
        return self.client.is_loaded()

    def is_active(self):
        """
        Returns true if a presentation is active and running.
        """
        log.debug('is active LibreOffice')
        return self.client.is_active()

    def unblank_screen(self):
        """
        Unblanks the screen.
        """
        log.debug('unblank screen LibreOffice')
        return self.client.unblank_screen()

    def blank_screen(self):
        """
        Blanks the screen.
        """
        log.debug('blank screen LibreOffice')
        self.client.blank_screen()

    def is_blank(self):
        """
        Returns true if screen is blank.
        """
        log.debug('is blank LibreOffice')
        return self.client.is_blank()

    def stop_presentation(self):
        """
        Stop the presentation, remove from screen.
        """
        log.debug('stop presentation LibreOffice')
        self.client.stop_presentation()

    def start_presentation(self):
        """
        Start the presentation from the beginning.
        """
        log.debug('start presentation LibreOffice')
        self.client.start_presentation()
        # Make sure impress doesn't steal focus, unless we're on a single screen setup
        if len(ScreenList().screen_list) > 1:
            Registry().get('main_window').activateWindow()

    def get_slide_number(self):
        """
        Return the current slide number on the screen, from 1.
        """
        return self.client.get_slide_number()

    def get_slide_count(self):
        """
        Return the total number of slides.
        """
        return self.client.get_slide_count()

    def goto_slide(self, slide_no):
        """
        Go to a specific slide (from 1).

        :param slide_no: The slide the text is required for, starting at 1
        """
        self.client.goto_slide(slide_no)

    def next_step(self):
        """
        Triggers the next effect of slide on the running presentation.
        """
        self.client.next_step()

    def previous_step(self):
        """
        Triggers the previous slide on the running presentation.
        """
        self.client.previous_step()

    def get_slide_text(self, slide_no):
        """
        Returns the text on the slide.

        :param slide_no: The slide the text is required for, starting at 1
        """
        return self.client.get_slide_text(slide_no)

    def get_slide_notes(self, slide_no):
        """
        Returns the text in the slide notes.

        :param slide_no: The slide the notes are required for, starting at 1
        """
        return self.client.get_slide_notes(slide_no)

