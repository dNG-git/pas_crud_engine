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

from dNG.data.supports_mixin import SupportsMixin
from dNG.runtime.not_implemented_exception import NotImplementedException

class Abstract(SupportsMixin):
    """
"Abstract" provides common methods for the "AccessControlValidator"
instance. It is used to validate access permissions at different stages of
CRUD execution including but not limited before and after element loading.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: crud_engine
:since:      v0.1.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def validate(self, crud_instance, operation, **kwargs):
        """
Validate access permissions for the requested operation and CRUD entity
instance specific data given.

:param crud_instance: CRUD entity instance
:param operation: CRUD operation requested including module and instance name

:since: v0.1.0
        """

        raise NotImplementedException()
    #
#
