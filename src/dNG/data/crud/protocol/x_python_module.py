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

import re

from dNG.data.crud.call_context import CallContext
from dNG.data.crud.instances.abstract import Abstract as AbstractInstance
from dNG.data.crud.operation_not_supported_exception import OperationNotSupportedException
from dNG.data.text.input_filter import InputFilter
from dNG.runtime.named_loader import NamedLoader

from .abstract import Abstract

class XPythonModule(Abstract):
    """
"XPythonModule" provides CRUD access to underlying Python runtime modules.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: crud_engine
:since:      v0.1.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    RE_NON_WORD_CHARS = re.compile("\\W+")
    """
RegExp to find non-word characters
    """

    def __init__(self, crud_url_elements):
        """
Constructor __init__(XPythonModule)

:param crud_url_elements: CRUD URL elements

:since: v0.1.0
        """

        Abstract.__init__(self, crud_url_elements)

        self._instance = None
        """
Underlying CRUD instance
        """
        self.operation_selector_list = [ ]
        """
List of path elements for the operation name executed
        """

        self.supported_features['access_control_validator'] = True

        path = (crud_url_elements.path[1:] if (crud_url_elements.path[:1] == "/") else crud_url_elements.path)
        path_elements = path.split("/")

        module_name = re.sub("\\W+", "_", path_elements.pop(0))

        instance_name = InputFilter.filter_control_chars(path_elements.pop(0).replace("-", "_"))
        instance_class_name = "".join([ word.capitalize() for word in instance_name.split("_") ])

        self._init_crud_instance(module_name, instance_class_name)

        if (len(path_elements) > 0):
            for selector in path_elements: self.operation_selector_list.append(InputFilter.filter_control_chars(selector))
        #
    #

    @property
    def access_control_validator(self):
        """
Returns the access control validator used for local CRUD entity instances.

:return: (object) Access control validator instance; None if not set
:since:  v0.1.0
        """

        return self._instance.access_control
    #

    @access_control_validator.setter
    def access_control_validator(self, validator):
        """
Sets the access control validator used for local CRUD entity instances.

:param validator: Access control validator instance

:since: v0.1.0
        """

        self._instance.access_control = validator
    #

    def __getattr__(self, name):
        """
python.org: Called when an attribute lookup has not found the attribute in
the usual places (i.e. it is not an instance attribute nor is it found in the
class tree for self).

:param name: Attribute name

:return: (mixed) Operation return value
:since:  v0.1.0
        """

        return self._get_call_stack_method(name)
    #

    def _get_call_stack(self, operation):
        """
Returns the list of methods to be called in sequence for the operation
requested.

:param operation: CRUD operation

:return: (list) List of methods to be called
:since:  v0.1.0
        """

        _return = [ ]
        operation = operation.lower()

        if (len(self.operation_selector_list) < 1):
            _return.append({ "method": self._get_crud_instance_method(operation),
                             "method_name": operation,
                             "select_id": None
                             })
        else:
            operation_selector_list = self.operation_selector_list.copy()

            while (len(operation_selector_list) > 0):
                operation_id_or_selector = operation_selector_list.pop()
                method_name = "{0}_{1}".format(operation, operation_id_or_selector)

                if (hasattr(self._instance, method_name)): operation_id_or_selector = None
                elif (len(operation_selector_list) > 0):
                    operation_selector = XPythonModule.RE_NON_WORD_CHARS.sub("_", operation_selector_list.pop())
                    method_name = "{0}_{1}".format(operation, operation_selector)

                    if (not hasattr(self._instance, method_name)): raise OperationNotSupportedException("Can't find match for operation call stack '{0}'".format(operation))
                else: method_name = operation

                _return.insert(0,
                               { "method": self._get_crud_instance_method(method_name),
                                 "method_name": method_name,
                                 "select_id": operation_id_or_selector
                               }
                              )

                operation = "select"
            #
        #

        if (self._instance.is_supported("call_stack_optimization")): _return = self._instance.optimize_call_stack(_return)
        return _return
    #

    def _get_call_stack_method(self, operation):
        """
Returns a callable for the generated stack of methods to be called for the
URL resource requested.

:param operation: CRUD operation

:return: (object) Python callable for the URL resource requested
:since:  v0.1.0
        """

        call_stack = self._get_call_stack(operation)

        def proxymethod(*_, **kwargs):
            updated_kwargs = kwargs.copy()

            for key in updated_kwargs:
                if (key[:1] == "_"): del(updated_kwargs[key])
            #

            is_first_call = True
            _return = None

            for call_definition in call_stack:
                updated_kwargs['_select_id'] = call_definition['select_id']
                updated_kwargs['_selected_value'] = (None if (is_first_call) else _return)

                with CallContext(self.context_manager_callee, call_definition['method_name']):
                    _return = call_definition['method'](**updated_kwargs)
                #

                is_first_call = False
            #

            return _return
        #

        return proxymethod
    #

    def _get_crud_instance_method(self, name):
        """
Returns the matching method of the underlying CRUD entity instance.

:param name: CRUD entity instance method name

:return: (object) CRUD entity instance method
:since:  v0.1.0
        """

        _return = getattr(self._instance, name, None)
        if (_return is None): raise OperationNotSupportedException("Operation '{0}' is not supported".format(name))

        return _return
    #

    def _init_crud_instance(self, module_name, instance_class_name):
        """
Initializes the underlying CRUD entity instance for the URL resource
requested.

:param module_name: CRUD entity module name
:param instance_class_name: CRUD entity class name

:since: v0.1.0
        """

        crud_instance = NamedLoader.get_instance("dNG.data.crud.instances.{0}.{1}".format(module_name, instance_class_name))
        if (not isinstance(crud_instance, AbstractInstance)): raise OperationNotSupportedException()

        self._instance = crud_instance
    #

    def is_supported(self, feature):
        """
Returns true if the feature requested is supported by this instance.

:param feature: Feature name string

:return: (bool) True if supported
:since:  v0.1.0
        """

        return (Abstract.is_supported(self, feature)
                if (feature in self.supported_features) else
                self._instance.is_supported(feature)
               )
    #
#
