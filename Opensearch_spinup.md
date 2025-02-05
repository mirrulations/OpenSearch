### Instructions on How To Spin Up an OpenSearch Serverless Instance
NOTE: Portions of this guide are to be changed to be more secure and efficient. This guide is a work in progress.

#### Step 1: Create an OpenSearch Service Collection
- Go to the OpenSearch Service Console at https://console.aws.amazon.com/opensearch-service/
- On the left side of the screen, under "Serverless", click on "Dashboard"
- Then click on "Create collection"
- Settings:
  - Collection name: Enter a name for your collection
  - Type: Search
  - Uncheck "Enable redundancy"
  - Click "Standard create"
  - For Ecryption, leave it as "Use AWS owned key" (This will be changed in the future)
  - For "Access collections from", select "Public" (This will be changed in the future)
  - Enable both access to Opensearch Dashboards and Endpoint
- Then click "Next"

#### Step 2: Configure Data Access
Note: This section is where you give permissions to perform actions on the collection. This will be modified in the future

- Name your rule
- click "Add principals"
    - Select "IAM users and roles"
    - Click on the search bar and select "Users" in the dropdown
    - Select your IAM user
    - Click "Save"
- Under "Grant permissions", select all that apply (For now, select all)
- Click "Next"
- You can add this rule as a new policy or add to an existing policy.
- Click "Next"
- Finally, click "Submit"

#### Step 3: Access the OpenSearch Dashboard

- Go back to the dashboard
- Click on the collection you just created
- Click on "OpenSearch Dashboards" on the top right
    - This will open a new tab with the OpenSearch Dashboards
    - Click on "Dev Tools" on the left side of the screen
    - You can now run queries on your collection in this environment
- Refer to this Official AWS Tutorial for more info on the basics of how to use OpenSearch Dashboards:
    - https://docs.aws.amazon.com/opensearch-service/latest/developerguide/quick-start.html