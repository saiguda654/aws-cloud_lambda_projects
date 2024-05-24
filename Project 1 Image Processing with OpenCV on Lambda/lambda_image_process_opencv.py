import os
import cv2
import boto3
import numpy as np

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the bucket and key from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Download the image from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    image_content = response['Body'].read()

    # Convert image content to numpy array
    nparr = np.frombuffer(image_content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert image to black and white
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Encode black and white image to bytes
    _, bw_image_bytes = cv2.imencode('.jpg', gray_img)

    # Upload the black and white image back to S3
    s3.put_object(Body=bw_image_bytes.tobytes(), Bucket=bucket, Key='black_and_white_' + key)

    return {
        'statusCode': 200,
        'body': f'Image converted to black and white and saved as black_and_white_{key}'
    }