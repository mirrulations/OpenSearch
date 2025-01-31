from opensearchpy import OpenSearch
import os
from dotenv import load_dotenv
import certifi


def create_client():
    load_dotenv()

    host = os.getenv('OPENSEARCH_HOST')
    port = os.getenv('OPENSEARCH_PORT')
    password = os.getenv('OPENSEARCH_INITIAL_PASSWORD')
    auth = ('admin', password)
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


client = create_client()
client.indices.delete(index='comments', ignore=[400, 404])