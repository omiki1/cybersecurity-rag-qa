from passlib.context import CryptContext
crypt = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password):
    return crypt.hash(password)
def verify_password(plain_password, hashed_password):
    return crypt.verify(plain_password, hashed_password)