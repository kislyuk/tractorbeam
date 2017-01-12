from __future__ import absolute_import, division, print_function, unicode_literals

import os, sys, datetime

USING_PYTHON2 = True if sys.version_info < (3, 0) else False

if USING_PYTHON2:
    from StringIO import StringIO
    from repr import Repr
    str = unicode # noqa
    from urlparse import urlparse
else:
    from io import StringIO
    from reprlib import Repr
    str = str
    from urllib.parse import urlparse
