import json
import boto3
import os

# Initialize the SNS client
sns_client = boto3.client('sns')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN') # We will set this in the Lambda console

def lambda_handler(event, context):
    try:
        # Extract details from the EventBridge event
        detail = event.get('detail', {})
        repository_name = detail.get('repository-name', 'Unknown Repo')
        image_tag = detail.get('image-tag', 'latest')

        message = f" Success: New Docker image pushed to ECR!\nRepository: {repository_name}\nTag: {image_tag}"

        # Send SNS Notification
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject='CI/CD Pipeline: ECR Push Successful'
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Notification sent successfully!')
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to process post-deployment task.')
        }
