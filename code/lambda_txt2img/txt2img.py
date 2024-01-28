import os
import sys
import subprocess
import io
import json
import base64
import boto3
import botocore


def lambda_handler(event, context):
    body = json.loads(event['body'])
    txtprompt = body['text_prompt']
    endpoint_name = body['endpoint_name']
    
    generated_image = generate_image(txtprompt, endpoint_name)
    message = {"prompt": txtprompt, 'image':generated_image}

    return {
        "statusCode": 200,
        "body": json.dumps(message),
        "headers": {
            "Content-Type": "application/json"
        }
    }


# ## amazon.titan-image-generator-v1 image generation
def generate_image(prompt: str, endpoint_name: str):
    
    bedrock = boto3.client(
        service_name="bedrock-runtime", region_name="us-east-1", endpoint_url=endpoint_name
        )
    bedrock_runtime = boto3.client(service_name="bedrock-runtime")
    

    body = json.dumps(
    {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": prompt,   # Required
            # "negativeText": negative_prompt  # Optional
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,   # Range: 1 to 5 
            "quality": "premium",  # Options: standard or premium
            "height": 768,         # Supported height list in the docs 
            "width": 1280,         # Supported width list in the docs
            "cfgScale": 5.0,       # Range: 1.0 (exclusive) to 10.0
            "seed": 0             # Range: 0 to 214783647
        }
    }
    )
    
    modelId = "amazon.titan-image-generator-v1"
    accept = "application/json"
    contentType = "application/json"

    try:
        response = bedrock.invoke_model(
            body=body, modelId=modelId, accept=accept, contentType=contentType
        )
        response_body = json.loads(response.get("body").read().decode())

    except botocore.exceptions.ClientError as error:

        if error.response['Error']['Code'] == 'AccessDeniedException':
            print(f"\x1b[41m{error.response['Error']['Message']}\
                    \nTo troubeshoot this issue please refer to the following resources.\
                    \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                    \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")
        else:
            raise error

    return response_body