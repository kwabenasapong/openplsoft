# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

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
# Frode Woldsund, Martin Zibricky                                             #
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
Provide a work around for a bug in QFileDialog
<https://bugs.launchpad.net/openlp/+bug/1209515>
"""
import os
import urllib

from PyQt4 import QtCore, QtGui

from openlp.core.lib.ui import UiStrings

class FileDialog(QtGui.QFileDialog):
    """
    Subclass QFileDialog to work round a bug
    """
    @staticmethod
    def getOpenFileNames(parent, title, path, filters):
        """
        Reimplement getOpenFileNames to fix the way it returns some file
        names that url encoded when selecting multiple files/
        """
        files = QtGui.QFileDialog.getOpenFileNames(parent, title, path, filters)
        file_list = QtCore.QStringList()
        for file in files:
            file = unicode(file)
            if not os.path.exists(file):
                file = urllib.unquote(file)
                if not os.path.exists(file):
                    QtGui.QMessageBox.information(parent,
                        UiStrings().FileNotFound,
                        UiStrings().FileNotFoundMessage % file)
                    continue
            file_list.append(QtCore.QString(file))
        return file_list