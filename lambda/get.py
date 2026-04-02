import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('imagemetadata')

BUCKET_NAME = "jeethu-imageapp-uploads"

def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response.get('Items', [])

        for item in items:
            item['fileUrl'] = f"https://{BUCKET_NAME}.s3.amazonaws.com/{item['s3Key']}"

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(items)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }