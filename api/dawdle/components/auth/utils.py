from passlib.hash import sha256_crypt


def encrypt_password(raw_password):
    return sha256_crypt.hash(raw_password)


def verify_password(user, password):
    if not password:
        return False
    return sha256_crypt.verify(password, user.password)
