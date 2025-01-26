
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

* Set your password as an environment variable for the `docker-compose` file.

  The `<password>` must have at least one upper, lower, number, and special characters and be at least 8 characters.

  ```
  export OPENSEARCH_INITIAL_ADMIN_PASSWORD=<password>
  ```
* Create a `.env` file containing:

  ```
  OPENSEARCH_INITIAL_PASSWORD=<password>
  ```

* Copy dockets from S3 (This step assumes you have the AWS CLI installed and configured).  In the root of this project run the following to download the data of two dockets.

  WARNING: DEA-2024-0059 is **LARGE** and will take a few minutes to download.

  ```
  aws s3 cp --recursive s3://mirrulations/DEA/DEA-2020-0008/ DEA-2020-0008 --no-sign-request
  aws s3 cp --recursive s3://mirrulations/DEA/DEA-2024-0059/ DEA-2024-0059 --no-sign-request
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

Data is stored in an external volume and will be retained if you stop the Docker containers.  Use the `delete_index.py` script to delete the data

  ```
  python delete_index.py
  ```
  
## Shutdown OpenSearch

To stop OpenSearch, run

  ```
  docker compose down
  ```
  
    
