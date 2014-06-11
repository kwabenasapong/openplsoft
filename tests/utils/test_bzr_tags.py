# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
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
Package to test for proper bzr tags.
"""
import os

from unittest import TestCase

from subprocess import Popen, PIPE

TAGS = [
    ['1.9.0', '1'],
    ['1.9.1', '775'],
    ['1.9.2', '890'],
    ['1.9.3', '1063'],
    ['1.9.4', '1196'],
    ['1.9.5', '1421'],
    ['1.9.6', '1657'],
    ['1.9.7', '1761'],
    ['1.9.8', '1856'],
    ['1.9.9', '1917'],
    ['1.9.10', '2003'],
    ['1.9.11', '2039'],
    ['1.9.12', '2063'],
    ['2.0', '2118'],
    ['2.0.1', '?'],
    ['2.0.2', '?'],
    ['2.0.3', '?'],
    ['2.0.4', '?'],
    ['2.1.0', '2119']
]


class TestBzrTags(TestCase):

    def bzr_tags_test(self):
        """
        Test for proper bzr tags
        """
        # GIVEN: A bzr branch
        path = os.path.dirname(__file__)

        # WHEN getting the branches tags
        bzr = Popen(('bzr', 'tags', '--directory=' + path), stdout=PIPE)
        stdout = bzr.communicate()[0]
        tags = [line.decode('utf-8').split() for line in stdout.splitlines()]

        # THEN the tags should match the accepted tags
        self.assertEqual(TAGS, tags, 'List of tags should match')