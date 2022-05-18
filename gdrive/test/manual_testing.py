import ssl

import pytest

from gdrive.auth import GoogleAuth
from gdrive.client import GDriveClient


# Run with python -m pytest gdrive/test/manual_testing.py

@pytest.fixture(scope="session")
def scopes():
    return ["https://www.googleapis.com/auth/drive"]


@pytest.fixture(scope="session")
def file_auth(scopes) -> GoogleAuth:
    secrets_file = "gdrive/test/credentials.json"
    token_file = "gdrive/test/token.pickle"
    yield GoogleAuth.from_settings(token_file, secrets_file, scopes)


@pytest.fixture(scope="session")
def secret_service_auth(scopes) -> GoogleAuth:
    secrets_url = "https://127.0.0.1:5000/secret?creds=gdrive"
    ctx = ssl.create_default_context()  # test only
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    token_file = "gdrive/test/token.pickle"
    yield GoogleAuth.from_settings(token_file, secrets_url, scopes, ctx)


@pytest.fixture(scope="session")
def client(secret_service_auth) -> GDriveClient:
    yield GDriveClient(secret_service_auth)


def test_file_auth(file_auth):
    assert file_auth.credentials.valid, "Expected not valid"
    assert not file_auth.credentials.expired, "Expected not expired"


def test_secretservice_auth(secret_service_auth):
    assert secret_service_auth.credentials.valid, "Expected not valid"
    assert not secret_service_auth.credentials.expired, "Expected not expired"


def test_upload(client):
    client.upload("gdrive:///a/b/", "README.md")
