import os
from dotenv import load_dotenv
import certifi
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

def create_client():
    load_dotenv()

    host = os.getenv('OPENSEARCH_HOST')
    port = os.getenv('OPENSEARCH_PORT')
    region = 'us-east-1'

    if host is None or port is None:
        raise ValueError('Please set the environment variables OPENSEARCH_HOST and OPENSEARCH_PORT')
    
    if host == 'localhost':
        auth = ('admin', os.getenv('OPENSEARCH_INITIAL_PASSWORD'))

        ca_certs_path = certifi.where()
        # Create the client with SSL/TLS enabled, but hostname verification disabled.
        client = OpenSearch(
            hosts = [{'host': host, 'port': port}],
            http_compress = True, # enables gzip compression for request bodies
            http_auth = auth,
            use_ssl = True,
            verify_certs = False,
            ssl_assert_hostname = False,
            ssl_show_warn = False,
            ca_certs = ca_certs_path
        )

        return client
    
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