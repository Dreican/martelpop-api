from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

try:
    hashed_password = ph.hash("my_secret_password")
    print(hashed_password)

    ph.verify(hashed_password, "my_secret_password")
    print("Password is valid")
except VerifyMismatchError:
    print("Invalid password")
