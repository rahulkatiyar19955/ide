import boto3

s3 = boto3.resource('s3')
for each_b in s3.buckets.all():
	print(each_b.name)
