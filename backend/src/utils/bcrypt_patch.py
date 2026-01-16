"""
bcrypt_patch.py

This module patches the bcrypt module to add the missing __about__ attribute
that passlib expects, resolving the compatibility issue between newer bcrypt
versions and older passlib versions.
"""

import bcrypt


def patch_bcrypt_for_passlib():
    """
    Patch bcrypt module to add the missing __about__ attribute that passlib expects.
    This resolves the AttributeError: module 'bcrypt' has no attribute '__about__'
    """
    if not hasattr(bcrypt, '__about__'):
        # Create a mock __about__ module-like object
        class About:
            __version__ = getattr(bcrypt, '__version__', '4.0.1')
        
        bcrypt.__about__ = About()


# Apply the patch when this module is imported
patch_bcrypt_for_passlib()