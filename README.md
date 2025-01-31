
## OpenSearch Exploration

This repo contains:

1. A docker-compose file (taken from the [OpenSearch Quickstart](https://opensearch.org/docs/latest/getting-started/quickstart/)) to run a local instance of OpenSearch
2. Python code to ingest the comments of a docket into a `comments` index
3. Python code to query the index to determine how many comments contain the term "drug"
4. Python code to delete the index.


## Setup

* Create a virtual environment and install libraries

  ```
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```
 ### Environment Variables

  The `<password>` must have at least one upper, lower, number, and special characters and be at least 8 characters.

  NOTE: including a `$` in the password as a special character leads to issues when running `docker compose` later on (the following text gets interpreted
  as a shell variable), so avoid using `$` in your password.

* Create a `.env` file containing:

  ```
  OPENSEARCH_INITIAL_PASSWORD=<password>
  OPENSEARCH_HOST=<hostname>
  OPENSEARCH_PORT=<port>
  S3_BUCKET_NAME=<bucket-name>
  ```
  
  
## Start OpenSearch

Based on the [quickstart](https://opensearch.org/docs/latest/getting-started/quickstart/).  I ignored step 1, and it worked fine on my laptop.

To start OpenSearch, make sure Docker is running and then run

  ```
  docker compose up -d
  ```

Check that you have three Docker containers running (See #4 of the [quickstart](https://opensearch.org/docs/latest/getting-started/quickstart/) for more info)

  ```
  docker compose ps
  ```
  
And confirm that you can communicate with the server (#5 of the [quickstart](https://opensearch.org/docs/latest/getting-started/quickstart/))

  ```
  curl https://localhost:9200 -ku admin:<custom-admin-password>
  ```  
  
## Ingest

With the virtual environment active and OpenSearch running via Docker, run the ingest script:

  ```
  python ingest.py
  ```
  
  This will produce one line of output per comment.  It takes a few minutes to complete.
  
## Query

The `query.py` script will query OpenSearch to determine how many comments match "drug" in each docket.

  ```
  python query.py
  ```

## Clean Up

Data is stored in an external volume and will be retained if you stop the Docker containers.  Use the `delete_client.py` script to delete the data

  ```
  python delete_client.py
  ```
  
## Shutdown OpenSearch

To stop OpenSearch, run

  ```
  docker compose down
  ```
  
    
