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

from dpt_runtime.exception_log_trap import ExceptionLogTrap

class CallContext(object):
    """
"CallContext" implements a context manager used to call pre and post methods
for CRUD requests.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: crud_engine
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, callee_instance, base_name = None):
        """
Constructor __init__(CallContext)

:param callee_instance: Callee instance
:param base_name: Method base name for "pre_*" and "post_*" calls

:since: v1.0.0
        """

        self.call_context_base_name = base_name
        """
Method base name
        """
        self.callee_instance = callee_instance
        """
Callee instance used for pre and post request methods if applicable.
        """
    #

    def __enter__(self):
        """
python.org: Enter the runtime context related to this object.

:since: v1.0.0
        """

        if (self.callee_instance is not None):
            with ExceptionLogTrap("pas_crud_engine"):
                method_name = ("pre_{0}".format(self.call_context_base_name)
                               if (self.call_context_base_name is not None) else
                               "_pre_call"
                              )

                _callable = getattr(self.callee_instance, method_name, None)
                if (callable(_callable)): _callable()
            #
        #
    #

    def __exit__(self, exc_type, exc_value, traceback):
        """
python.org: Exit the runtime context related to this object.

:return: (bool) True to suppress exceptions
:since:  v1.0.0
        """

        if (self.callee_instance is not None):
            with ExceptionLogTrap("pas_crud_engine"):
                method_name = ("post_{0}".format(self.call_context_base_name)
                               if (self.call_context_base_name is not None) else
                               "_post_call"
                              )

                _callable = getattr(self.callee_instance, method_name, None)

                if (callable(_callable)):
                    kwargs = { }

                    if (exc_type is not None or exc_value is not None):
                        kwargs['exception'] = { "type": exc_type, "value": exc_value, "traceback": traceback }
                    #

                    _callable(**kwargs)
                #
            #
        #

        return False
    #
#
