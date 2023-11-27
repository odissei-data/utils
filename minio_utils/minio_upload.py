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
parser.add_argument('--bucket', type=str, dest='bucket',
                    help='Bucket')
args = parser.parse_args()

minio_client = boto3.client('s3',
                            endpoint_url=args.minio_url,
                            aws_access_key_id=args.minio_user,
                            aws_secret_access_key=args.minio_password
                            )

local_directory = args.path
bucket_name = args.bucket
success_count = 0

for root, dirs, files in os.walk(local_directory):
    for file in files:
        if not file.startswith('.DS_Store'):
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_directory)
            s3_path = relative_path.replace('\\', '/')

            try:
                minio_client.upload_file(local_path, bucket_name, s3_path)
                success_count += 1
                print(f"Uploaded: {local_path}")
            except Exception as e:
                print(f"Failed to upload: {local_path}. Error: {str(e)}")

print(f"Total files uploaded: {success_count}")
