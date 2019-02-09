# -*- coding: utf-8 -*-

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;crud_engine

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasCrudEngineVersion)#
#echo(__FILEPATH__)#
"""

# pylint: disable=import-error

from .abstract_filter_parser import AbstractFilterParser

class FlatFilterParser(AbstractFilterParser):
    """
"FlatFilterParser" provides a condition definition based on a flat
dictionary.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: crud_engine
:since:      v0.1.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def _parse_and_concatenation(self, filter_data):
        """
Parses the given dictionary representing an "and" concatenated filter
definition.

:param filter_data: "and" concatenated dictionary

:return: (mixed) Parser specific filter representation
:since:  v0.1.0
        """

        _return = { }

        for key in filter_data:
            _return[key] = self._parse(key, filter_data[key])
        #

        return _return
    #

    def _set_empty_filter(self):
        """
Sets an empty parser specific filter representation for an empty filter
string.

:since: v0.1.0
        """

        self._filter = { }
    #
#
