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

from .access_denied_exception import AccessDeniedException
from .input_validation_exception import InputValidationException
from .nothing_matched_exception import NothingMatchedException
from .operation_failed_exception import OperationFailedException
from .operation_not_supported_exception import OperationNotSupportedException
from .resource import Resource
