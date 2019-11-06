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

from functools import wraps

from dpt_runtime.io_exception import IOException
from dpt_runtime.not_implemented_exception import NotImplementedException
from dpt_runtime.operation_not_supported_exception import OperationNotSupportedException as _OperationNotSupportedException
from dpt_runtime.supports_mixin import SupportsMixin
from dpt_runtime.type_exception import TypeException

from ..access_controls.abstract import Abstract as AbstractAccessControlValidator
from ..access_denied_exception import AccessDeniedException
from ..input_validation_exception import InputValidationException
from ..operation_failed_exception import OperationFailedException
from ..operation_not_supported_exception import OperationNotSupportedException

class Abstract(SupportsMixin):
    """
"Abstract" provides default methods for CRUD entity instances.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: crud_engine
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    UNDERSCORE_ATTRIBUTE_KEYS = [ ]
    """
List of attribute names for this CRUD entity instance which start with an underscore.
    """

    __slots__ = [ "_access_control_instance" ] + SupportsMixin._mixin_slots_
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self):
        """
Constructor __init__(Abstract)

:since: v1.0.0
        """

        SupportsMixin.__init__(self)

        self._access_control_instance = None
        """
The "AccessControlValidator" instance to be called.
        """

        self.supported_features['access_control_validation'] = self._supports_access_control_validation
    #

    @property
    def access_control(self):
        """
Returns the "AccessControlValidator" instance to be called to validate
access permissions at different stages of CRUD execution including but not
limited before and after element loading.

:return: (mixed) AccessControlValidator instance; None if not defined
:since:  v1.0.0
        """

        return self._access_control_instance
    #

    @access_control.setter
    def access_control(self, validator):
        """
Sets the "AccessControlValidator" instance to be called.

:param validator: AccessControlValidator instance

:since: v1.0.0
        """

        if (not isinstance(validator, AbstractAccessControlValidator)): raise TypeException("Access control validator given is invalid")
        self._access_control_instance = validator
    #

    def _supports_access_control_validation(self):
        """
Returns false if no access control validation is supported.

:return: (bool) True if access control validation is supported
:since:  v1.0.0
        """

        return (self.access_control is not None)
    #

    @classmethod
    def _get_filtered_kwargs(cls, kwargs):
        """
Returns all kwargs after filtering keys and their values.

:param cls: Python class
:param kwargs: Keyword arguments to filter

:return: (dict) Filtered kwargs
:since:  v1.0.0
        """

        return dict(( key, kwargs[key] ) for key in kwargs if (key[:1] != "_" and key not in cls.UNDERSCORE_ATTRIBUTE_KEYS))
    #

    @staticmethod
    def restrict_to_access_control_validated_execution(_callable):
        """
Restricts access to the callable to valid users.

:param _callable: Wrapped code

:return: (object) Proxy method
:since:  v1.0.0
    """

        @wraps(_callable)
        def proxymethod(self, *args, **kwargs):
            if (not self.is_supported("access_control_validation")): raise AccessDeniedException()
            return _callable(self, *args, **kwargs)
        #

        return proxymethod
    #

    @staticmethod
    def catch_and_wrap_matching_exception(_callable):
        """
Catch certain exceptions and wrap them in CRUD defined ones.

:param _callable: Wrapped code

:return: (object) Proxy method
:since:  v1.0.0
    """

        @wraps(_callable)
        def proxymethod(self, *args, **kwargs):
            try: return _callable(self, *args, **kwargs)
            except ( OperationFailedException, OperationNotSupportedException ): raise
            except NotImplementedException as handled_exception: raise OperationNotSupportedException(_exception = handled_exception)
            except _OperationNotSupportedException as handled_exception: raise OperationNotSupportedException(_exception = handled_exception)
            except IOException as handled_exception: raise OperationFailedException(_exception = handled_exception)
            except TypeError as handled_exception: raise InputValidationException(_exception = handled_exception)
            except ValueError as handled_exception: raise InputValidationException(_exception = handled_exception)
        #

        return proxymethod
    #
#
