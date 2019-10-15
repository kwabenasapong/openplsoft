#!/bin/sh
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
#
# This script generates qm files from ts files.  These are not for comitting
# but for testing only.
#
###############################################################################
pwd=`pwd`
result=${PWD##*/}; echo $result

if [ $result != 'scripts' ] ; then
	echo 'This script must be run from the scripts directory'
	exit
fi

cd ../resources/i18n

rm *.qm

for file in *.ts;
 do echo $file
  lconvert-qt5 -i $file -o ${file%%ts}qm ;
  done