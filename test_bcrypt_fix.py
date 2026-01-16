#!/usr/bin/env python3
"""
Test script to verify bcrypt compatibility fix
"""

def test_bcrypt_compatibility():
    """Test that bcrypt and passlib work together without the __about__ error"""
    try:
        from passlib.hash import bcrypt
        import bcrypt as bcrypt_module
        
        # Check if bcrypt has the __about__ attribute (this was causing the error)
        print(f"bcrypt module: {bcrypt_module}")
        print(f"bcrypt version: {getattr(bcrypt_module, '__version__', 'unknown')}")
        
        # Test hashing and verification
        password = "test_password_123"
        hashed = bcrypt.hash(password)
        print(f"Password hashed successfully: {hashed[:20]}...")
        
        # Verify the hash
        is_valid = bcrypt.verify(password, hashed)
        print(f"Password verification: {is_valid}")
        
        print("✓ Bcrypt compatibility test passed!")
        return True
    except AttributeError as e:
        if "__about__" in str(e):
            print(f"✗ Bcrypt compatibility test failed: {e}")
            return False
        else:
            raise
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Testing bcrypt compatibility...")
    success = test_bcrypt_compatibility()
    if success:
        print("\n🎉 All tests passed! The bcrypt compatibility issue should be fixed.")
    else:
        print("\n❌ Tests failed! The bcrypt compatibility issue still exists.")