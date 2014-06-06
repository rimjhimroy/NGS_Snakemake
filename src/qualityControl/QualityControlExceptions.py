"""
@version: 1.0
@author: Jetse

This python module contains all exceptions which can be raised by the quality control.
"""

class FileFormatException(Exception):
    """
    The file is not in the expected format.
    """
    pass