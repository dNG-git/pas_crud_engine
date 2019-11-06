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

from .operation_failed_exception import OperationFailedException

class UpdateConflictException(OperationFailedException):
    """
Exception if the CRUD operation detects a concurrent update conflict.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: crud_engine
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, value = "A concurrent update conflict prevented the requested operation", _exception = None):
        """
Constructor __init__(UpdateConflictException)

:param value: Exception message value
:param _exception: Inner exception

:since: v1.0.0
        """

        OperationFailedException.__init__(self, value, _exception)
    #
#
