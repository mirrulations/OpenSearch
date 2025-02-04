from create_client import create_client


client = create_client()
client.indices.delete(index='comments', ignore=[400, 404])