"""
Module defines the utility functions used in roguehostapd
"""

import contextlib
import io
import sys

@contextlib.contextmanager
def nostdout():
    """
    Hide the stdout in the specific context

    :return: None
    :rtype: None
    """
    save_stdout = sys.stdout
    sys.stdout = io.BytesIO()
    yield
    sys.stdout = save_stdout
