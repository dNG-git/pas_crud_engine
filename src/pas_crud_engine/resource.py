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

try: from collections.abc import Mapping
except ImportError: from collections import Mapping

try: from urllib.parse import urlsplit
except ImportError: from urlparse import urlsplit

from dpt_module_loader import NamedClassLoader
from dpt_runtime.binary import Binary

from .operation_failed_exception import OperationFailedException
from .operation_not_supported_exception import OperationNotSupportedException
from .protocol import Abstract

class Resource(object):
    """
"Resource" provides CRUD access to the requested URL resource.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: crud_engine
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    OPERATIONS_SUPPORTED = [ "create", "delete", "execute", "get", "is_valid", "update", "upsert" ]

    def __init__(self, crud_url):
        """
Constructor __init__(Resource)

:param crud_url: CRUD URL to query

:since: v1.0.0
        """

        self._instance = None
        """
CRUD URL entity instance
        """
        self._path = None
        """
CRUD URL entity path
        """
        self._protocol = None
        """
CRUD URL scheme protocol
        """
        self._url = crud_url
        """
CRUD URL
        """

        if ("://" not in crud_url):
            if (crud_url[:1] != "/"): crud_url = "/{0}".format(crud_url)
            crud_url = "x-python-module://{0}".format(crud_url)
        #

        crud_url_elements = urlsplit(crud_url)

        self._path = crud_url_elements.path
        self._protocol = crud_url_elements.scheme.replace("-", "_")

        self._init_protocol_instance(crud_url_elements)
    #

    @property
    def access_control_validator(self):
        """
Returns the access control validator used for local CRUD entity instances.

:return: (object) Access control validator instance; None if not set
:since:  v1.0.0
        """

        if (not self._instance.is_supported("access_control_validator")): raise OperationNotSupportedException()
        return self._instance.access_control_validator
    #

    @access_control_validator.setter
    def access_control_validator(self, validator):
        """
Sets the access control validator used for local CRUD entity instances.

:param validator: Access control validator instance

:since: v1.0.0
        """

        if (not self._instance.is_supported("access_control_validator")): raise OperationNotSupportedException()
        self._instance.access_control_validator = validator
    #

    @property
    def context_manager_callee(self):
        """
Returns the callee instance set.

:return: (object) Callee instance; None if not defined
:since:  v1.0.0
        """

        return self._instance.context_manager_callee
    #

    @context_manager_callee.setter
    def context_manager_callee(self, callee_instance):
        """
Sets the callee instance used for pre and post request methods.

:param callee_instance: Callee instance

:since: v1.0.0
        """

        self._instance.context_manager_callee = callee_instance
    #

    def __getattr__(self, name):
        """
python.org: Called when an attribute lookup has not found the attribute in
the usual places (i.e. it is not an instance attribute nor is it found in the
class tree for self).

:param name: Attribute name

:return: (mixed) Operation return value
:since:  v1.0.0
        """

        def proxymethod(*_, **kwargs): return self.call(name, **kwargs)
        return proxymethod
    #

    def call(self, operation, **kwargs):
        """
Executes the given operation for the initialized CRUD URL entity instance.

:param operation: CRUD operation

:return: (mixed) Operation return value
:since:  v1.0.0
        """

        operation = Binary.str(operation)
        if (type(operation) is not str): raise OperationNotSupportedException()
        operation = operation.lower()

        if (operation not in self.__class__.OPERATIONS_SUPPORTED): raise OperationNotSupportedException("Operation '{0}' is not supported".format(operation))

        try: _callable = getattr(self._instance, operation)
        except AttributeError as handled_exception: raise OperationNotSupportedException("Operation '{0}' is not supported".format(operation), _exception = handled_exception)

        return _callable(**kwargs)
    #

    def _init_protocol_instance(self, crud_url_elements):
        """
Initializes the protocol instance responsible for routing the CRUD URL
requests for this instance.

:param crud_url_elements: CRUD URL elements

:since: v1.0.0
        """

        protocol_class_name = NamedClassLoader.get_camel_case_class_name(self._protocol)

        protocol_instance = NamedClassLoader.get_instance_in_namespace("crud", "protocol.{0}".format(protocol_class_name), crud_url_elements = crud_url_elements)
        if (not isinstance(protocol_instance, Abstract)): raise OperationFailedException("CRUD protocol '{0}' is not supported".format(self._protocol))

        self._instance = protocol_instance
    #

    def is_operation_supported(self, operation):
        """
Returns true if the operation is defined.

:param operation: CRUD operation

:return: (mixed) True if operation is defined
:since:  v1.0.0
        """

        operation = Binary.str(operation)
        if (type(operation) is not str): raise OperationNotSupportedException()
        operation = operation.lower()

        try: _return = (operation in self.__class__.OPERATIONS_SUPPORTED and hasattr(self._instance, operation))
        except OperationNotSupportedException: _return = False

        return _return
    #

    def is_supported(self, feature):
        """
Returns true if the feature requested is supported by this instance.

:param feature: Feature name string

:return: (bool) True if supported
:since:  v1.0.0
        """

        return self._instance.is_supported(feature)
    #

    def set_access_control_validator(self, validator):
        """
Sets the access control validator used for local CRUD entity instances.

:param validator: Access control validator instance

:return: (object) Resource instance for chaining
:since:  v1.0.0
        """

        self.access_control_validator = validator
        return self
    #

    def set_context_manager_callee(self, callee_instance):
        """
Sets the callee instance used for pre and post request methods.

:param callee_instance: Callee instance

:return: (object) Resource instance for chaining
:since:  v1.0.0
        """

        self.context_manager_callee = callee_instance
        return self
    #
#
