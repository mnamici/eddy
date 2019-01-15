# -*- coding: utf-8 -*-

##########################################################################
#                                                                        #
#  Eddy: a graphical editor for the specification of Graphol ontologies  #
#  Copyright (C) 2015 Daniele Pantaleone <danielepantaleone@me.com>      #
#                                                                        #
#  This program is free software: you can redistribute it and/or modify  #
#  it under the terms of the GNU General Public License as published by  #
#  the Free Software Foundation, either version 3 of the License, or     #
#  (at your option) any later version.                                   #
#                                                                        #
#  This program is distributed in the hope that it will be useful,       #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
#  GNU General Public License for more details.                          #
#                                                                        #
#  You should have received a copy of the GNU General Public License     #
#  along with this program. If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
#  #####################                          #####################  #
#                                                                        #
#  Graphol is developed by members of the DASI-lab group of the          #
#  Dipartimento di Ingegneria Informatica, Automatica e Gestionale       #
#  A.Ruberti at Sapienza University of Rome: http://www.dis.uniroma1.it  #
#                                                                        #
#     - Domenico Lembo <lembo@dis.uniroma1.it>                           #
#     - Valerio Santarelli <santarelli@dis.uniroma1.it>                  #
#     - Domenico Fabio Savo <savo@dis.uniroma1.it>                       #
#     - Daniele Pantaleone <pantaleone@dis.uniroma1.it>                  #
#     - Marco Console <console@dis.uniroma1.it>                          #
#                                                                        #
##########################################################################

"""
Collection of utility functions to deal with XML documents.
"""

import re

from PyQt5 import QtXmlPatterns

# TODO: Move to regex module
RE_NCNAME_CHAR = re.compile(r'([a-zA-Z]|:|_|\d|_|-|\.)')
RE_NCNAME_START_CHAR = re.compile(r'([a-zA-Z]|:|_)')


def getNCNamePrefix(s):
    """
    Returns the longest NCName that is the prefix of the given string.

    :type s: str
    :rtype str:
    """
    # Do not split blank nodes
    if len(s) > 1 and s[0] == '_' and s[1] == ':':
        return s

    localPartStartIndex = getNCNameSuffixIndex(s)
    if localPartStartIndex > -1:
        prefix = s[0:localPartStartIndex]
    else:
        prefix = s

    if prefix.endswith(':'):
        return prefix[:-1]
    else:
        return prefix


def getNCNameSuffix(s):
    """
    Returns the longest NCName that is the suffix of the given string.

    :type s: str
    :rtype str:
    """
    # Do not split blank nodes
    if len(s) > 1 and s[0] == '_' and s[1] == ':':
        return None

    localPartStartIndex = getNCNameSuffixIndex(s)
    if localPartStartIndex > -1:
        return s[localPartStartIndex:]
    else:
        return None


def getNCNameSuffixIndex(s):
    """
    Returns the start index of the longest NCName that is the suffix of the given string,
    or -1 if the suffix is not an NCName.

    :type s: str
    :rtype: int
    """
    if len(s) > 1 and s[0] == '_' and s[1] == ':':
        return -1
    index = -1

    for i in range(len(s) - 1, -1, -1):
        if s[i] != ':' and RE_NCNAME_START_CHAR.match(s[i]):
            index = i
        if s[i] == ':' or RE_NCNAME_CHAR.match(s[i]) is None:
            break
    return index


def isNCName(s):
    """
    Returns `True if the given string is an NCName, and `False` otherwise.

    :type s: str
    :rtype: bool
    """
    return s and QtXmlPatterns.QXmlName.isNCName(s)


def isQName(s):
    """
    Returns `True` if the given string is a QName, or `False` otherwise.
    A QName is either an NCName, or an NCName followed by a colon followed by an NCName (i.e. prefix:localname).

    :type s: str
    :rtype: bool
    """
    if s is None or len(s) == 0:
        return False

    foundColon = False
    inNCName = False
    for i in range(0, len(s)):
        if s[i] == ':':
            # Only a single colon is allowed in QNames to separate NCNames
            if foundColon:
                return False
            foundColon = True

            # End of previous NCName
            if not inNCName:
                return False
            inNCName = False
        else:
            if not inNCName:
                # Check that char after : is a valid NCName start char
                if not RE_NCNAME_START_CHAR.match(s[i]):
                    return False
                else: # Begin parsing NCName
                    inNCName = True
            else:
                # Check that next char is still a valid NCName char
                if not RE_NCNAME_CHAR.match(s[i]):
                    return False
    return True


def splitQName(s):
    pass
