"""Helper functions."""
from passlib.context import CryptContext


def hash(password: str) -> str:
    """Hashes password based on the passlib bcrypt hashing algo."""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def verify(plain_pw: str, hashed_pw: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_pw, hashed_pw)
