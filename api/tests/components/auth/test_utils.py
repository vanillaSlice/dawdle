from dawdle.components.auth.utils import (create_initials, encrypt_password,
                                          verify_password)
from tests.utils import fake


class TestUtils:

    #
    # encrypt_password / verify_password tests.
    #

    def test_encrypt_password_verify_password(self):
        password = fake.password()
        encrypted_password = encrypt_password(password)
        assert password != encrypted_password
        assert verify_password(encrypted_password, password)

    def test_encrypt_password_verify_password_incorrect(self):
        password = fake.password()
        encrypted_password = encrypt_password(password)
        assert password != encrypted_password
        assert not verify_password(encrypted_password, "wrong")

    def test_verify_password_None(self):
        encrypted_password = encrypt_password(fake.password())
        assert not verify_password(encrypted_password, None)

    #
    # create_initials tests.
    #

    def test_create_initials(self):
        assert create_initials(" john  peter smith richard  david ") == "JPSR"
