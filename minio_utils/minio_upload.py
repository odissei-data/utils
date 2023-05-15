import argparse
import boto3
import os

parser = argparse.ArgumentParser(
    description="Upload files to a specified minio bucket")
parser.add_argument('--url', type=str, dest='minio_url',
                    help='URL of the minio server you want to upload to')
parser.add_argument('--username', type=str, dest='minio_user', help='username')
parser.add_argument('--password', type=str, dest='minio_password',
                    help='password')
parser.add_argument('--path', type=str, dest='path',
                    help='Path to where the data you want to upload lives')
parser.add_argument('--prefix', type=str, dest='prefix',
                    help='Object prefix used in the bucket')
args = parser.parse_args()

minio_client = boto3.client('s3',
                            endpoint_url=args.minio_url,
                            aws_access_key_id=args.minio_user,
                            aws_secret_access_key=args.minio_password
                            )

local_directory = args.path
bucket_name = 'harvested-metadata'
object_prefix = args.prefix

for root, dirs, files in os.walk(local_directory):
    for file in files:
        if not file.startswith('.DS_Store'):
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_directory)
            s3_path = os.path.join(object_prefix, relative_path).replace('\\',
                                                                         '/')
            minio_client.upload_file(local_path, bucket_name, s3_path)
