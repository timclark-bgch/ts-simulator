import json
import os

import boto3
import botocore.config
import tempfile

pipeline = boto3.client('codepipeline')
sns = boto3.client('sns')


def package(event, *_):
	print json.dumps(event)

	job = event['CodePipeline.job']['id']

	try:
		job_data = event['CodePipeline.job']['data']
		__source_to_s3(job_data)

		pipeline.put_job_success_result(jobId=job, executionDetails={'summary': 'Artifacts stored'})

		return "Success"
	except Exception as e:
		print e.message
		pipeline.put_job_failure_result(jobId=job, failureDetails={'type': 'JobFailed', 'message': e.message})

	return "Failure"


def __source_to_s3(job_data):
	session = boto3.Session(aws_access_key_id=job_data['artifactCredentials']['accessKeyId'],
													aws_secret_access_key=job_data['artifactCredentials']['secretAccessKey'],
													aws_session_token=job_data['artifactCredentials']['sessionToken'])

	s3 = session.client('s3', region_name='eu-west-1', config=botocore.config.Config(signature_version='s3v4'))

	source = job_data['inputArtifacts'][0]['location']['s3Location']
	revision = job_data['inputArtifacts'][0]['revision']

	source_key = source['objectKey']
	dest_key = '{}/{}'.format(os.environ['storage_folder'], source_key.split('/')[-1])

	with tempfile.NamedTemporaryFile() as tmp_file:
		s3.download_file(source['bucketName'], source_key, tmp_file.name)
		boto3.client('s3').upload_file(tmp_file.name, os.environ['storage_bucket'], dest_key,
																	 ExtraArgs={'Metadata': {'commit': revision}})


target_environments = {
	'staging': {'role': 'role'},
	'production': {'role': 'role'}
}


def release(event, *_):
	print json.dumps(event)
	print os.environ['sns_topic']

	for record in event['Records']:
		bucket = record['s3']['bucket']['name']
		key = record['s3']['object']['key']

		for target in target_environments.keys():
			message = {'target': target, 'bucket': bucket, 'key': key}
			response = sns.publish(TopicArn=os.environ['sns_topic'], Message=json.dumps(message))
			print "Published - {}".format(response)


def transfer(event, *_):
	print json.dumps(event)
