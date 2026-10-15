import io
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import create_app
from storage.local_backend import LocalBackend


def make_client(tmp_path):
    return create_app(LocalBackend(str(tmp_path))).test_client()


def test_upload_list_download_delete(tmp_path):
    c = make_client(tmp_path)
    c.post("/api/upload", data={"prefix": "", "files": (io.BytesIO(b"hello"), "a.txt")},
           content_type="multipart/form-data")
    files = c.get("/api/list").get_json()["files"]
    assert files[0]["name"] == "a.txt" and files[0]["size"] == 5
    assert c.get("/api/download?key=a.txt").data == b"hello"
    c.post("/api/delete", json={"key": "a.txt"})
    assert c.get("/api/list").get_json()["files"] == []


def test_folders(tmp_path):
    c = make_client(tmp_path)
    c.post("/api/folder", json={"prefix": "", "name": "docs"})
    assert c.get("/api/list").get_json()["folders"][0]["key"] == "docs/"


def test_path_traversal_blocked(tmp_path):
    c = make_client(tmp_path)
    assert c.get("/api/list?prefix=../../").status_code == 400
