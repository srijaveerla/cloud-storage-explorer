# ☁️ Cloud Storage Explorer

A web-based file manager for cloud storage. Browse folders, upload (drag & drop), download, delete and filter files in an
**Amazon S3 bucket**, or in a **local folder** (so you can demo it without any cloud account).

Built with **Python, Flask, boto3** and a single-page HTML/JS interface.

## Features
- Folder navigation with breadcrumbs
- Upload (button or drag & drop), download, delete, create folder, live filter
- Pluggable backends: `local` (default) and `s3`
- Secure S3 downloads using short-lived presigned URLs
- Path-traversal protection and 50 MB upload limit
- Automated tests (pytest)

## Project structure
| Path | Purpose |
|---|---|
| `app.py` | Flask app and REST API |
| `storage/local_backend.py` | Local-folder backend |
| `storage/s3_backend.py` | Amazon S3 backend (boto3) |
| `templates/index.html` | Web interface |
| `tests/test_app.py` | Tests |

## Run locally
```bash
python -m venv .venv
.venv\Scripts\activate          # Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Use a real S3 bucket
1. Install the AWS CLI and run `aws configure` (never put keys in code).
2. Create an S3 bucket in the AWS console.
3. Run:
```bash
set STORAGE_BACKEND=s3          # Mac/Linux: export STORAGE_BACKEND=s3
set S3_BUCKET=your-bucket-name
set AWS_REGION=ap-south-1
python app.py
```
The IAM user needs `s3:ListBucket`, `s3:GetObject`, `s3:PutObject`, `s3:DeleteObject` on the bucket.

## Tests
```bash
pytest -q
```

## Future work
Login/authentication, multi-bucket switcher, Azure Blob and Google Cloud Storage backends, file preview, storage-usage dashboard.

## License
MIT
