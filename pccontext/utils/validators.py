"""
This module contains custom validators
"""

import re

__all__ = ["check_ada_handle_format"]


def check_ada_handle_format(handle):
    """
    Checks if the handle is in the correct format
    :param handle: AdaHandle with optional SubHandles
    :return:
    """
    pattern = r"^\$[a-z0-9_.-]{1,15}(@[a-z0-9_.-]{1,15})?$"  # define regex pattern
    if handle is not None and bool(re.match(pattern, handle.lower())):
        return handle
    else:
        raise ValueError(
            f"Invalid AdaHandle format: {handle} (must be in the format $handle or $handle@subhandle)"
        )
