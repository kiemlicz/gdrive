import pytest
from pykeepass import PyKeePass

from gdrive.auth import GoogleAuth
from gdrive.client import GDriveClient

# Run with python -m pytest gdrive/test/manual_testing.py

@pytest.fixture(scope="session")
def scopes():
    return ["https://www.googleapis.com/auth/drive"]


@pytest.fixture(scope="session")
def kdbx_dependencies():
    kdbx_file = "gdrive/test/test.kdbx"
    password = "secret"
    kdbx = PyKeePass(kdbx_file, password)
    yield kdbx, "/gdrive", "token.pickle", "credentials.json"


@pytest.fixture(scope="session")
def kdbx_auth(kdbx_dependencies, scopes):
    kdbx, path, token_attachment, secrets_attachment = kdbx_dependencies
    yield GoogleAuth.from_kdbx(kdbx, path, token_attachment, secrets_attachment, scopes)


@pytest.fixture(scope="session")
def file_auth(scopes):
    secrets_file = "gdrive/test/credentials.json"
    token_file = "gdrive/test/token.pickle"
    yield GoogleAuth.from_settings_file(token_file, secrets_file, scopes)


@pytest.fixture(scope="session")
def secretstorage_auth(scopes):
    attributes = {"kdbx": "credentials"}
    token_file = "gdrive/test/token.pickle"
    yield GoogleAuth.from_secretservice(attributes, token_file, scopes)


@pytest.fixture(scope="session")
def client(kdbx_auth):
    yield GDriveClient(kdbx_auth)


def test_kdbx_auth(kdbx_auth):
    assert kdbx_auth.credentials.valid, "Expected not valid"
    assert not kdbx_auth.credentials.expired, "Expected not expired"


def test_file_auth(file_auth):
    assert file_auth.credentials.valid, "Expected not valid"
    assert not file_auth.credentials.expired, "Expected not expired"


def test_secretservice_auth(secretstorage_auth):
    assert secretstorage_auth.credentials.valid, "Expected not valid"
    assert not secretstorage_auth.credentials.expired, "Expected not expired"
