import os


def get_backend():
    """Choose backend from env: STORAGE_BACKEND=local (default) or s3."""
    kind = os.environ.get("STORAGE_BACKEND", "local").lower()
    if kind == "s3":
        from .s3_backend import S3Backend
        return S3Backend(os.environ["S3_BUCKET"], os.environ.get("AWS_REGION"))
    from .local_backend import LocalBackend
    return LocalBackend(os.environ.get("LOCAL_ROOT", "local_storage"))
