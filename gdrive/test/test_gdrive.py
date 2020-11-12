import re
from typing import List, Dict, Any

import pytest

from google.oauth2.service_account import Credentials
from gdrive.auth import GoogleAuth
from gdrive.client import GDriveClient


class TestService:
    class TestFilesResult:
        def __init__(self, result):
            self.result = result

        def execute(self):
            return self.result

    class TestFiles:
        def __init__(self, outer):
            self.query_regex = re.compile("\'(\S+)\' in parents")
            self.files_tree = outer.files_tree

        def _find(self, f_id: str) -> Dict[str, Any]:
            def go(files: List[Dict[str, Any]]) -> Dict[str, Any] or None:
                if not files:
                    return None
                matching = [e for e in files if e['id'] == f_id]
                if matching:
                    return matching[0]
                else:
                    children = [f['files'] for f in files]
                    l = [go(f) for f in children]
                    return next(e for e in l if e is not None)

            return go(self.files_tree)

        def list(self, q):
            search = self.query_regex.search(q)
            if search:
                parent_id = search.group(1)
                result = self._find(parent_id)
                if result is None:
                    raise RuntimeError(f"{q} returned nothing")
                result['incompleteSearch'] = False
                return TestService.TestFilesResult(result)
            else:
                raise RuntimeError("Missing test data")

        def export(self, fileId: str, mimeType: str):
            return TestService.TestFilesResult(self._find(fileId)['content'])

        def get_media(self, fileId: str):
            return self.export(fileId, None)

    def __init__(self, files_tree):
        self.files_tree = files_tree

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def files(self):
        return TestService.TestFiles(self)


@pytest.fixture(scope="session")
def files():
    yield [{
        'id': 'root',
        'files': [
            {'name': "path", 'id': '1', 'files': [
                {'name': "file", "id": '4', 'files': [], 'content': b"filecontent", "mimeType": "text/plain"},
                {'name': "file2", "id": '5', 'files': [], 'content': b"file2content", "mimeType": "text/plain"},
                {'name': "dir1", "id": '6', 'files': [
                    {'name': "file3", "id": '7', 'files': [], 'content': b"file3content", "mimeType": "text/plain"},
                    {'name': "dir2", "id": '8', 'files': [
                        {'name': "file4", "id": '9', 'files': [], 'content': b"file4content", "mimeType": "text/plain"},
                    ], 'mimeType': "application/vnd.google-apps.folder"},
                ], 'mimeType': "application/vnd.google-apps.folder"},
            ], 'mimeType': "application/vnd.google-apps.folder"},
            {'name': "otherpath", 'id': '2', 'files': [], 'content': b"otherpathcontent", "mimeType": "text/plain"},
            {'name': "bla", 'id': '3', 'files': [], 'content': b"blacontent", "mimeType": "text/plain"}
        ], 'mimeType': "application/vnd.google-apps.folder"
    }]


@pytest.fixture(scope="session")
def client():
    cred = Credentials(None, None, None)
    auth = GoogleAuth(cred)
    c = GDriveClient(auth)
    yield c


def test_file_get(client: GDriveClient, files, mocker):
    s = TestService(files)
    with mocker.patch.object(client, 'service', s):
        file = client.get("gdrive://path/file?mime_type=text/plain")
        assert file == "filecontent", f"Assert failed, expected: filecontent, but received: {file}"


def test_walk(client: GDriveClient, files, mocker):
    s = TestService(files)
    with mocker.patch.object(client, 'service', s):
        files = client.walk("gdrive://path/dir1", "/")
        nested = [f['content'] for f in files if f['mimeType'] == 'application/vnd.google-apps.folder']
        assert len(files) == 2
        assert len(nested) == 1
        assert nested[0][0]['content'] == b'file4content'
