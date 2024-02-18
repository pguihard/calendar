"""
Called when an exception occurred
"""
import sys

def e_line_number():
    """
    return the line number
    """
    __, __, e_traceback = sys.exc_info()
    return e_traceback.tb_lineno
