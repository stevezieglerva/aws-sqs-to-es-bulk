import boto3


def lambda_handler(event, context):
	print("Started")
	count = 0
	for message in event["Records"]:
		count = count + 1
		print(str(count) + ". " + message["body"])
	print("Finished")
	return "Success"