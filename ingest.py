
import os
import json
from dotenv import load_dotenv
import certifi
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3


def ingest(client, document):
    response = client.index(index = 'comments', body = document, refresh = True)
    print(response)


def create_client():
    load_dotenv()

    host = os.getenv('OPENSEARCH_HOST')
    port = os.getenv('OPENSEARCH_PORT')
    region = 'us-east-1'

    service = 'aoss'
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, region, service)


    # Create the client with SSL/TLS enabled, but hostname verification disabled.
    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_compress = True, # enables gzip compression for request bodies
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        pool_maxsize=20,
    )

    return client

def ingest_comment(client, bucket, key):
    obj = bucket.Object(key)
    file_text = obj.get()['Body'].read().decode('utf-8')
    data = json.loads(file_text)
    document = {
        'comment': data['data']['attributes']['comment'],
        'agencyId': data['data']['attributes']['agencyId'],
        'docketId': data['data']['attributes']['docketId'],
        'modifyDate': data['data']['attributes']['modifyDate'],
        'id': data['data']['id']
    }
    ingest(client, document)

def ingest_all_comments(client, bucket):
    for obj in bucket.objects.all():
        if obj.key.endswith('.json') and ('/comments/' in obj.key):
            ingest_comment(client, bucket, obj.key)


if __name__ == '__main__':
    client = create_client()

    s3 = boto3.resource(
        service_name = 's3',
        region_name = 'us-east-1'
    )

    print('boto3 created')

    bucket = s3.Bucket(os.getenv('S3_BUCKET_NAME'))

    ingest_all_comments(client, bucket)
