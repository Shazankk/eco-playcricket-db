import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Check if we have the keys to our cloud box
required_env_vars = [
    "CLOUDFLARE_ACCOUNT_ID", 
    "CLOUDFLARE_R2_BUCKET",
    "CLOUDFLARE_ACCESS_KEY",
    "CLOUDFLARE_SECRET_KEY"
]

for var in required_env_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {var}")

# Connect to our cloud picture box
s3 = boto3.client(
    's3',
    endpoint_url=f"https://{os.getenv('CLOUDFLARE_ACCOUNT_ID')}.r2.cloudflarestorage.com",
    aws_access_key_id=os.getenv('CLOUDFLARE_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('CLOUDFLARE_SECRET_KEY'),
    region_name="auto"
)

def check_file_exists(key):
    """Check if a picture already exists in our cloud box"""
    try:
        print(f"Checking if {key} exists in bucket {os.getenv('CLOUDFLARE_R2_BUCKET')}")
        s3.head_object(
            Bucket=os.getenv('CLOUDFLARE_R2_BUCKET'),
            Key=key
        )
        print(f"File {key} exists in R2 storage")
        return True
    except Exception as e:
        # If we get a 404, the file doesn't exist
        if hasattr(e, 'response') and e.response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 404:
            print(f"File {key} does not exist in R2 storage")
            return False
        # Any other error is a problem
        print(f"Error checking if file exists: {str(e)}")
        raise

def upload_image_to_r2(file_buffer, key, content_type="image/jpeg"):
    """Put a picture in our cloud box"""
    try:
        print(f"Uploading {key} to bucket {os.getenv('CLOUDFLARE_R2_BUCKET')}")
        
        # Check if picture already exists
        if check_file_exists(key):
            raise ValueError(
                f"File {key} already exists in R2 storage. Please contact Shashank to handle new picture request."
            )
        
        # Upload the picture
        s3.put_object(
            Bucket=os.getenv('CLOUDFLARE_R2_BUCKET'),
            Key=key,
            Body=file_buffer,
            ContentType=content_type
        )
        
        # Create the web link to the picture
        image_url = f"https://{os.getenv('CLOUDFLARE_R2_BUCKET')}.{os.getenv('CLOUDFLARE_ACCOUNT_ID')}.r2.cloudflarestorage.com/{key}"
        
        print("Upload complete, URL:", image_url)
        return image_url
    except Exception as e:
        print(f"R2 upload error: {str(e)}")
        raise