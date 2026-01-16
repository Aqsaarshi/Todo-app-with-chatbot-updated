#!/usr/bin/env python3
"""
Patch for bcrypt compatibility issue
"""

def patch_bcrypt():
    """
    Patch bcrypt module to add the missing __about__ attribute
    that passlib expects to read version information
    """
    import bcrypt
    
    # Add the missing __about__ attribute if it doesn't exist
    if not hasattr(bcrypt, '__about__'):
        # Create a mock __about__ module-like object
        class About:
            __version__ = getattr(bcrypt, '__version__', '4.0.1')
        
        bcrypt.__about__ = About()
        print("Patched bcrypt module with __about__ attribute")

if __name__ == "__main__":
    patch_bcrypt()
    print("Bcrypt patch applied successfully")
    
    # Now test that passlib can work with bcrypt
    from passlib.hash import bcrypt as bcrypt_passlib
    password = "test_password_123"
    hashed = bcrypt_passlib.hash(password)
    print(f"Password hashed successfully with passlib: {hashed[:20]}...")
    
    is_valid = bcrypt_passlib.verify(password, hashed)
    print(f"Password verification: {is_valid}")
    print("✓ Bcrypt compatibility issue should be resolved!")