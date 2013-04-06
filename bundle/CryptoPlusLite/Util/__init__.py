"""Util initialization

makes the Util modules from Crypto AND CryptoPlus available here
"""
#import Crypto
#from Crypto.Util import number, randpool, RFC1751
import util

from pkg_resources import parse_version

__all__ = ["util"]

#if parse_version(Crypto.__version__) > parse_version("2.0.1"):
#        from Crypto.Util import python_compat
#        __all__.append("python_compat")

#del Crypto
