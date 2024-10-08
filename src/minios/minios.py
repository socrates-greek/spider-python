from minio import Minio
from minio.error import S3Error


class MinioStorage:
    def __init__(self, endpoint, access_key, secret_key, secure=False):
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)
        self.endpoint = endpoint  # 保存 endpoint 以便后续使用

    def create_bucket(self, bucket_name):
        """创建存储桶，如果已存在则不再创建。"""
        if self.client.bucket_exists(bucket_name):
            print(f"Bucket '{bucket_name}' already exists.")
            return
        try:
            self.client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        except S3Error as e:
            print(f"Error creating bucket: {e}")

    def upload_file(self, bucket_name, file_path, object_name):
        try:
            self.client.fput_object(bucket_name, object_name, file_path)
            print(f"Uploaded {file_path} to {bucket_name}/{object_name}")

            # 返回可访问的 URL
            url = f"http://{self.endpoint}/{bucket_name}/{object_name}"
            return url
        except S3Error as e:
            print(f"Error uploading file: {e}")
            return None

    def download_file(self, bucket_name, object_name, file_path):
        try:
            self.client.fget_object(bucket_name, object_name, file_path)
            print(f"Downloaded {bucket_name}/{object_name} to {file_path}")
        except S3Error as e:
            print(f"Error downloading file: {e}")

    def list_objects(self, bucket_name):
        try:
            objects = self.client.list_objects(bucket_name)
            return [obj.object_name for obj in objects]
        except S3Error as e:
            print(f"Error listing objects: {e}")
            return []

    def delete_object(self, bucket_name, object_name):
        try:
            self.client.remove_object(bucket_name, object_name)
            print(f"Deleted {bucket_name}/{object_name}")
        except S3Error as e:
            print(f"Error deleting object: {e}")


# 示例用法
if __name__ == "__main__":
    # 替换为你的 MinIO 配置
    endpoint = 'your-minio-endpoint:9000'
    access_key = 'your-access-key'
    secret_key = 'your-secret-key'

    storage = MinioStorage(endpoint, access_key, secret_key)

    # 创建存储桶
    storage.create_bucket('my-bucket-picture')

    # 上传文件并获取可访问 URL
    url = storage.upload_file('my-bucket-picture', 'local-file.txt', 'remote-file.txt')
    if url:
        print(f"可访问的 URL: {url}")

    # 列出存储桶中的对象
    objects = storage.list_objects('my-bucket-picture')
    print(objects)

    # 下载文件
    storage.download_file('my-bucket', 'remote-file.txt', 'downloaded-file.txt')

    # 删除文件
    storage.delete_object('my-bucket', 'remote-file.txt')
