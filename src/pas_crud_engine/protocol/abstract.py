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

from dpt_runtime.supports_mixin import SupportsMixin

class Abstract(SupportsMixin):
    """
"Abstract" provides basic CRUD resource methods for protocol
implementations.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: crud_engine
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, crud_url_elements):
        """
Constructor __init__(Abstract)

:param crud_url_elements: CRUD URL elements

:since: v1.0.0
        """

        SupportsMixin.__init__(self)

        self._context_manager_callee_instance = None
        """
Callee instance used for pre and post request methods if applicable.
        """
    #

    @property
    def context_manager_callee(self):
        """
Returns the callee instance set.

:return: (object) Callee instance; None if not defined
:since:  v1.0.0
        """

        return self._context_manager_callee_instance
    #

    @context_manager_callee.setter
    def context_manager_callee(self, callee_instance):
        """
Sets the callee instance used for pre and post request methods.

:param callee_instance: Callee instance

:since: v1.0.0
        """

        self._context_manager_callee_instance = callee_instance
    #
#
