from __future__ import absolute_import
from future.standard_library import suspend_hooks
from future.utils import PY3

if PY3:
    from zatudan.support import *
else:
    __future_module__ = True
    with suspend_hooks():
        from zatudan.test_support import *
