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

from unittest import TestCase

from mock import MagicMock

from openlp.plugins.songs.lib.duplicatesongfinder import DuplicateSongFinder

class TestLib(TestCase):

    def songs_probably_equal_test(self):
        """
        Test the DuplicateSongFinder.songs_probably_equal function.
        """
        full_lyrics =u'''amazing grace how sweet the sound that saved a wretch like me i once was lost but now am
        found was blind but now i see  twas grace that taught my heart to fear and grace my fears relieved how
        precious did that grace appear the hour i first believed  through many dangers toils and snares i have already
        come tis grace that brought me safe thus far and grace will lead me home'''
        short_lyrics =u'''twas grace that taught my heart to fear and grace my fears relieved how precious did that
        grace appear the hour i first believed'''
        error_lyrics =u'''amazing how sweet the trumpet that saved a wrench like me i once was losst but now am
        found waf blind but now i see  it was grace that taught my heart to fear and grace my fears relieved how
        precious did that grace appppppppear the hour i first believedxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx snares i have
        already come to this grace that brought me safe so far and grace will lead me home'''
        different_lyrics=u'''on a hill far away stood an old rugged cross the emblem of suffering and shame and i love
        that old cross where the dearest and best for a world of lost sinners was slain  so ill cherish the old rugged
        cross till my trophies at last i lay down i will cling to the old rugged cross and exchange it some day for a
        crown'''
        dsf = DuplicateSongFinder()
        song1 = MagicMock()
        song2 = MagicMock()
        
        #GIVEN: Two equal songs
        song1.search_lyrics = full_lyrics
        song2.search_lyrics = full_lyrics
        
        #WHEN: We compare those songs for equality
        result = dsf.songs_probably_equal(song1, song2)
        
        #THEN: The result should be True
        assert result is True, u'The result should be True'
        
        #GIVEN: A song and a short version of the same song
        song1.search_lyrics = full_lyrics
        song2.search_lyrics = short_lyrics
        
        #WHEN: We compare those songs for equality
        result = dsf.songs_probably_equal(song1, song2)
        
        #THEN: The result should be True
        assert result  is True, u'The result should be True'
        
        #GIVEN: A song and the same song with lots of errors
        song1.search_lyrics = full_lyrics
        song2.search_lyrics = error_lyrics
        
        #WHEN: We compare those songs for equality
        result = dsf.songs_probably_equal(song1, song2)
        
        #THEN: The result should be True
        assert result is True, u'The result should be True'
        
        #GIVEN: Two different songs
        song1.search_lyrics = full_lyrics
        song2.search_lyrics = different_lyrics
        
        #WHEN: We compare those songs for equality
        result = dsf.songs_probably_equal(song1, song2)
        
        #THEN: The result should be False
        assert result is False, u'The result should be False'
