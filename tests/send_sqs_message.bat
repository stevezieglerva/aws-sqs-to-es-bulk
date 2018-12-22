call aws sqs send-message --queue-url https://sqs.us-east-1.amazonaws.com/112280397275/code-index --message-body " https://s3.amazonaws.com/code-index/prep-output/ProjectX/sqs_test_single.txt"

rem call aws sqs send-message-batch --queue-url https://sqs.us-east-1.amazonaws.com/112280397275/code-index --entries file://test_batch_messages.json

