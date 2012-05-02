# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
The :mod:`powersongimport` module provides the functionality for importing
PowerSong songs into the OpenLP database.
"""
import logging

from openlp.core.lib import translate
from openlp.plugins.songs.lib.songimport import SongImport

log = logging.getLogger(__name__)

class PowerSongImport(SongImport):
    """
    The :class:`PowerSongImport` class provides the ability to import song files
    from PowerSong.

    **PowerSong Song File Format:**

    The file has a number of label-field pairs of variable length.

    Labels and Fields:
        * Every label and field is preceded by an integer which specifies its
          byte-length.
        * If the length < 128 bytes, only one byte is used to encode
          the length integer.
        * But if it's greater, as many bytes are used as necessary:
            * the first byte = (length % 128) + 128
            * the next byte = length / 128
            * another byte is only used if (length / 128) >= 128
            * and so on (3 bytes needed iff length > 16383)

    Metadata fields:
        * Every PowerSong file begins with a TITLE field.
        * This is followed by zero or more AUTHOR fields.
        * The next label is always COPYRIGHTLINE, but its field may be empty.
          This field may also contain a CCLI number: e.g. "CCLI 176263".

    Lyrics fields:
        * Each verse is contained in a PART field.
        * Lines have Windows line endings ``CRLF`` (0x0d, 0x0a).
        * There is no concept of verse types.

    Valid extensions for a PowerSong song file are:
        * .song
    """

    def doImport(self):
        """
        Receive a list of files to import.
        """
        if not isinstance(self.importSource, list):
            return
        self.importWizard.progressBar.setMaximum(len(self.importSource))
        for file in self.importSource:
            if self.stopImportFlag:
                return
            self.setDefaults()
            parse_error = False
            with open(file, 'rb') as self.song_file:
                # Get title to check file is valid PowerSong song format
                label, field = self.readLabelField()
                if label == u'TITLE':
                    self.title = field.replace(u'\n', u' ')
                else:
                    self.logError(file, unicode(
                        translate('SongsPlugin.PowerSongSongImport', \
                        'Invalid PowerSong file. Missing "TITLE" header.')))
                    continue
                # Get rest of fields from file
                while True:
                    label, field = self.readLabelField()
                    if not label:
                        break
                    if label == u'AUTHOR':
                        self.parseAuthor(field)
                    elif label == u'COPYRIGHTLINE':
                        found_copyright = True
                        self.parseCopyrightCCLI(field)
                    elif label == u'PART':
                        self.addVerse(field)
                    else:
                        parse_error = True
                        self.logError(file, unicode(
                            translate('SongsPlugin.PowerSongSongImport', \
                            '"%s" Invalid PowerSong file. Unknown header: "%s".'
                            % (self.title, label))))
                        break
                if parse_error:
                    continue
                # Check that file had COPYRIGHTLINE label
                if not found_copyright:
                    self.logError(file, unicode(
                        translate('SongsPlugin.PowerSongSongImport', \
                        '"%s" Invalid PowerSong file. Missing "COPYRIGHTLINE" \
                         header.' % self.title)))
                    continue
                # Check that file had at least one verse
                if not self.verses:
                    self.logError(file, unicode(
                        translate('SongsPlugin.PowerSongSongImport', \
                        '"%s" Verses not found. Missing "PART" header.'
                        % self.title)))
                    continue
            if not self.finish():
                self.logError(file)

    def readLabelField(self):
        """
        Read (as a 2-tuple) the next two variable-length strings
        """
        label = unicode(self.song_file.read(
            self.readLength()), u'utf-8', u'ignore')
        if label:
            field = unicode(self.song_file.read(
                self.readLength()), u'utf-8', u'ignore')
        else:
            field = u''
        return label, field

    def readLength(self):
        """
        Read the byte-length of the next variable-length string

        If at the end of the file, returns 0.
        """
        this_byte = self.song_file.read(1)
        if not this_byte:
            return 0
        this_byte_val = ord(this_byte)
        if this_byte_val < 128:
            return this_byte_val
        else:
            return (self.readLength() * 128) + (this_byte_val - 128)

    def parseCopyrightCCLI(self, field):
        """
        Look for CCLI song number, and get copyright
        """
        copyright, sep, ccli_no = field.rpartition(u'CCLI')
        if not sep:
            copyright = ccli_no
            ccli_no = u''
        if copyright:
            self.addCopyright(copyright.rstrip(u'\n').replace(u'\n', u' '))
        if ccli_no:
            ccli_no = ccli_no.strip(u' :')
            if ccli_no.isdigit():
                self.ccliNumber = ccli_no
