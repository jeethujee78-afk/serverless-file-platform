import json
import boto3
import base64
import uuid
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

BUCKET_NAME = "jeethu-imageapp-uploads"
TABLE_NAME = "imagemetadata"

table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)

        file_name = body["fileName"]
        file_data = body["fileData"]
        content_type = body.get("contentType", "application/octet-stream")

        # Handle data URL or pure base64
        if "," in file_data:
            file_data = file_data.split(",")[1]

        file_bytes = base64.b64decode(file_data)

        image_id = str(uuid.uuid4())
        s3_key = f"uploads/{image_id}_{file_name}"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=file_bytes,
            ContentType=content_type
        )

        table.put_item(
            Item={
                "imageid": image_id,  # must match table key
                "fileName": file_name,
                "s3Key": s3_key,
                "uploadedAt": datetime.utcnow().isoformat(),
                "contentType": content_type
            }
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({"message": "Upload successful"})
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }