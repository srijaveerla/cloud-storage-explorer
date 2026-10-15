"""Amazon S3 backend. Credentials come from `aws configure` or env vars (never hard-code keys)."""
import boto3


class S3Backend:
    name = "s3"

    def __init__(self, bucket, region=None):
        self.bucket = bucket
        self.s3 = boto3.client("s3", region_name=region)

    def list(self, prefix=""):
        prefix = prefix.strip("/")
        prefix = prefix + "/" if prefix else ""
        folders, files = [], []
        paginator = self.s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix, Delimiter="/"):
            for cp in page.get("CommonPrefixes", []):
                key = cp["Prefix"]
                folders.append({"name": key[len(prefix):].rstrip("/"), "key": key})
            for obj in page.get("Contents", []):
                if obj["Key"] == prefix:
                    continue
                files.append({"name": obj["Key"][len(prefix):], "key": obj["Key"], "size": obj["Size"],
                              "modified": obj["LastModified"].strftime("%Y-%m-%d %H:%M")})
        return folders, files

    def upload(self, prefix, filename, stream):
        prefix = prefix.strip("/")
        key = (prefix + "/" if prefix else "") + filename
        self.s3.upload_fileobj(stream, self.bucket, key)

    def download_url(self, key):
        return self.s3.generate_presigned_url(
            "get_object", Params={"Bucket": self.bucket, "Key": key}, ExpiresIn=300)

    def delete(self, key):
        if key.endswith("/"):  # delete everything under the folder
            paginator = self.s3.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=self.bucket, Prefix=key):
                objs = [{"Key": o["Key"]} for o in page.get("Contents", [])]
                if objs:
                    self.s3.delete_objects(Bucket=self.bucket, Delete={"Objects": objs})
        else:
            self.s3.delete_object(Bucket=self.bucket, Key=key)

    def create_folder(self, prefix, name):
        prefix = prefix.strip("/")
        self.s3.put_object(Bucket=self.bucket, Key=(prefix + "/" if prefix else "") + name + "/")
