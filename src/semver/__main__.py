"""
Module to support call with :file:`__main__.py`. Used to support the following
call::

    $ python3 -m semver ...

This makes it also possible to "run" a wheel like in this command::

    $ python3 semver-3*-py3-none-any.whl/semver -h

"""

import os.path
import sys
from typing import List, Optional

if __package__ in (None, ""):
    # When this file is executed as a plain script (for example, directly
    # from an extracted wheel), the ``semver`` package is not importable
    # yet. Extend ``sys.path`` *before* importing ``semver.cli`` below,
    # otherwise the import fails with ModuleNotFoundError.
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path[0:0] = [path]

from semver import cli


def main(cliargs: Optional[List[str]] = None) -> int:
    return cli.main(cliargs)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
