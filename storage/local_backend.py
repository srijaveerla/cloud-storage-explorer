"""Local-folder backend: behaves like a bucket, so the app works with no cloud account."""
import os
import shutil
from datetime import datetime


class LocalBackend:
    name = "local"

    def __init__(self, root):
        self.root = os.path.abspath(root)
        os.makedirs(self.root, exist_ok=True)

    def _safe(self, key):
        """Resolve key inside root; block path traversal like ../../etc."""
        path = os.path.abspath(os.path.join(self.root, key.strip("/")))
        if path != self.root and not path.startswith(self.root + os.sep):
            raise ValueError("Invalid path")
        return path

    def list(self, prefix=""):
        path = self._safe(prefix)
        folders, files = [], []
        if not os.path.isdir(path):
            return folders, files
        for entry in sorted(os.scandir(path), key=lambda e: e.name.lower()):
            if entry.name == ".gitkeep":
                continue
            key = (prefix.strip("/") + "/" if prefix.strip("/") else "") + entry.name
            if entry.is_dir():
                folders.append({"name": entry.name, "key": key + "/"})
            else:
                st = entry.stat()
                files.append({"name": entry.name, "key": key, "size": st.st_size,
                              "modified": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M")})
        return folders, files

    def upload(self, prefix, filename, stream):
        os.makedirs(self._safe(prefix), exist_ok=True)
        dest = self._safe((prefix.strip("/") + "/" if prefix.strip("/") else "") + filename)
        with open(dest, "wb") as f:
            shutil.copyfileobj(stream, f)

    def download_path(self, key):
        path = self._safe(key)
        return path if os.path.isfile(path) else None

    def delete(self, key):
        path = self._safe(key)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    def create_folder(self, prefix, name):
        os.makedirs(self._safe((prefix.strip("/") + "/" if prefix.strip("/") else "") + name), exist_ok=True)
