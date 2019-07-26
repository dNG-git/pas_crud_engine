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

from dpt_json import JsonResource
from dpt_runtime.binary import Binary
from dpt_runtime.supports_mixin import SupportsMixin
from dpt_threading.thread_lock import ThreadLock

from ..input_validation_exception import InputValidationException
from ..operation_not_supported_exception import OperationNotSupportedException

class AbstractFilterParser(SupportsMixin):
    """
"AbstractFilterParser" provides common methods to parse and generate an
CRUD instance specific condition definition.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: crud_engine
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, filter_string):
        """
Constructor __init__(AbstractFilterParser)

:param filter_string: Raw JSON filter definition

:since: v1.0.0
        """

        SupportsMixin.__init__(self)

        filter_string = Binary.str(filter_string)
        if (not isinstance(filter_string, str)): raise InputValidationException("Filter given is invalid")

        self._blacklisted_keys = [ ]
        """
List of keys marked as blacklisted
        """
        self._filter = None
        """
Parser specific filter representation
        """
        self._raw_filter_string = filter_string.strip()
        """
Raw JSON filter definition
        """
        self._lock = ThreadLock()
        """
Thread safety lock
        """

        if (len(self._raw_filter_string) < 1): self._set_empty_filter()
    #

    @property
    def filter(self):
        """
Returns the parser specific filter representation for the raw filter string
given.

:return: (mixed) Parser specific filter representation
:since:  v1.0.0
        """

        if (self._filter is None): self._parse_raw_filter_string()
        return self._filter
    #

    def add_blacklisted_key(self, key):
        """
Adds the given key to the filter blacklist.

:param key: Key to be blacklisted

:since: v1.0.0
        """

        if (key not in self._blacklisted_keys):
            with self._lock:
                # Thread safety
                if (key not in self._blacklisted_keys): self._blacklisted_keys.append(key)
            #
        #
    #

    def _parse(self, key, filter_data):
        """
Parses the given filter data representing an value or sub-condition.

:param key: Key of filter level being parsed
:param filter_data: Filter data

:return: (mixed) Parser specific filter representation
:since:  v1.0.0
        """

        _return = None

        if (key not in self._blacklisted_keys):
            filter_data_type = type(filter_data)

            if (filter_data_type is dict): _return = self._parse_and_concatenation(filter_data)
            elif (filter_data_type is list): _return = self._parse_or_concatenation(key, filter_data)
            else: _return = filter_data
        #

        return _return
    #

    def _parse_and_concatenation(self, filter_data):
        """
Parses the given dictionary representing an "and" concatenated filter
definition.

:param filter_data: "and" concatenated dictionary

:return: (mixed) Parser specific filter representation
:since:  v1.0.0
        """

        raise OperationNotSupportedException()
    #

    def _parse_or_concatenation(self, key, filter_list):
        """
Parses the given list representing an "or" concatenated filter definition.

:param key: Key of filter level being parsed
:param filter_list: "or" concatenated list

:return: (mixed) Parser specific filter representation
:since:  v1.0.0
        """

        raise OperationNotSupportedException()
    #

    def _parse_raw_filter_string(self):
        """
Parses the top-level raw JSON filter definition.

:since:  v1.0.0
        """

        if (self._filter is None):
            if (self._raw_filter_string[:1] not in ( "[", "{" ) or self._raw_filter_string[-1:] not in ( "]", "}" )):
                raise InputValidationException("Filter definition given is invalid")
            #

            self._filter = self._parse(None, JsonResource.json_to_data(self._raw_filter_string))
            if (self._filter is None): raise InputValidationException("Failed to parse filter definition given")
        #
    #

    def remove_blacklisted_key(self, key):
        """
Removes the given key from the filter blacklist.

:param key: Blacklisted key

:since:  v1.0.0
        """

        if (key in self._blacklisted_keys):
            with self._lock:
                # Thread safety
                if (key in self._blacklisted_keys): self._blacklisted_keys.remove(key)
            #
        #
    #

    def _set_empty_filter(self):
        """
Sets an empty parser specific filter representation for an empty filter
string.

:since: v1.0.0
        """

        raise OperationNotSupportedException()
    #
#
