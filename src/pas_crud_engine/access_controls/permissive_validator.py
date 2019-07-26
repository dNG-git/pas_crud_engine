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

from dpt_runtime.type_exception import TypeException

from .abstract import Abstract
from ..access_denied_exception import AccessDeniedException

class PermissiveValidator(Abstract):
    """
The "PermissiveValidator" allows access as long as the requested operation
is not blacklisted.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: crud_engine
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self):
        """
Constructor __init__(PermissiveValidator)

:since: v1.0.0
        """

        Abstract.__init__(self)

        self._blacklisted_operations = [ ]
        """
Blacklisted operations which will cause an "AccessDeniedException".
        """

        self.supported_features['blacklisting'] = True
    #

    @property
    def blacklisted_operations(self):
        """
Returns a list of blacklisted operations which will cause an
"AccessDeniedException".

:return: (List) Blacklisted operations
:since:  v1.0.0
        """

        return self._blacklisted_operations
    #

    @blacklisted_operations.setter
    def blacklisted_operations(self, operations):
        """
Sets the list of blacklisted operations which will cause an
"AccessDeniedException".

:param operations: List of blacklisted operations

:since: v1.0.0
        """

        if (not isinstance(operations, list)): raise TypeException("List of blacklisted operations given is invalid")
        self._blacklisted_operations = operations
    #

    def validate(self, crud_instance, operation, **kwargs):
        """
Validate access permissions for the requested operation and CRUD entity
instance specific data given.

:param crud_instance: CRUD entity instance
:param operation: CRUD operation requested including module and instance
       name

:since: v1.0.0
        """

        if (operation in self._blacklisted_operations): raise AccessDeniedException("Operation '{0}' is blacklisted".format(operation))
    #
#
