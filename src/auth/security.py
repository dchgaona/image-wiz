from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def verify_password(plain, hashed):
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain, hashed)

async def hash_password(password):
    """Hash a plain password."""
    return pwd_context.hash(password)