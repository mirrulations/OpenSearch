
import os
import json
from dotenv import load_dotenv
import certifi
from opensearchpy import OpenSearch




def make_document(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
        # make a new dict with data.attributes.comment, data.attributes.agencyId, data.attributes.docketId, data.attributes.docketId.modifyDate, and data.id
        document = {
            'comment': data['data']['attributes']['comment'],
            'agencyId': data['data']['attributes']['agencyId'],
            'docketId': data['data']['attributes']['docketId'],
            'modifyDate': data['data']['attributes']['modifyDate'],
            'id': data['data']['id']
        }

        # print the new dict
        return document


def ingest(client, document):
    response = client.index(index = 'comments', body = document, refresh = True)
    print(response)


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


def walk_to_ingest(client, root):
    subfolder = 'text-{}/comments'.format(root)
    root = os.path.join(root, subfolder)
    print(root)
    for path, dirs, files in os.walk(root):
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(path, file)
                ingest(client, make_document(filepath))


if __name__ == '__main__':
    client = create_client()
    walk_to_ingest(client, 'DEA-2020-0008')
    walk_to_ingest(client, 'DEA-2024-0059')
