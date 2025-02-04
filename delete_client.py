from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import os
from dotenv import load_dotenv
import certifi
import boto3


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


client = create_client()
client.indices.delete(index='comments', ignore=[400, 404])