import boto3


def lambda_handler(event, context):
	print("Started")
	for message in event["Records"]:
		print(message["body"])
	return "Success"