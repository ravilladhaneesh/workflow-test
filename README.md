# workflow-test


This repo is used for learning the Github CI/CD, to automate the deployment of AWS infrastructure using terraform.

The workflow file in this repo is actually used in [github-repo-manager](#github-repo-manager) projects to deploy AWS resources.

## github-repo-manager

github-repo-manager is a system that automates the collection and storage of GitHub repository metadata in a database, with a
responsive website for users to view and analyze the stored data. The system ensures seamless integration
between data retrieval, storage, and visualization, providing an efficient and user-friendly interface.

1. [github-data-processor](https://github.com/ravilladhaneesh/github-data-processor)
2. [github-data-controller](https://github.com/ravilladhaneesh/github-data-controller)
3. [github-data-viewer](https://github.com/ravilladhaneesh/github-data-viewer)


### Detailed Description of the job

1. The below code snippet describes the name of the workflow as 'Python Test' and the workflow runs on each push to 'main' branch.You can update/Add branch as your requirement to run the worklow for your specific branch.

        name: Python Test

        on:
        push:
            branches:
            - main  # Run the workflow when code is pushed to the main branch

2. The below code snippet has the jobs that runs in the workflow. In this script we have a single job 'run-python-script' that executes the [github-data-processor](https://github.com/ravilladhaneesh/github-data-processor) project to put data to AWS.The job is deployed in the 'staging' environment(Update the environment that you have created in the above [Steps to put data to AWS](https://github.com/ravilladhaneesh/github-data-controller?tab=readme-ov-file#steps-to-put-data-to-aws) section).The permissions section in the code snippet are required to request the JWT token to autenticate AWS and read content of the repository.

        jobs:
            run-python-script:
                runs-on: ubuntu-latest
                environment: staging
                permissions:
                    id-token: write
                    contents: read

3. The below code snippet describes the executions of the job.In the step 1. the job checkouts the current repository and in step 2. github-data-processor is cloned into the current job execution environment.


        steps:
        # Step 1: Checkout the repository
        - name: Checkout code
            uses: actions/checkout@v3

        # Step 2: Clone github-data-processor repo
        - name: Clone github-data-processor repository
            run: git clone https://github.com/ravilladhaneesh/github-data-processor.git

4. This is the step where the autentication for AWS is requested using [Github OpenID Connect](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services) with the 'AWS_PUT_DATA_ROLE'. The AWS_PUT_DATA_ROLE, AWS_REGION variable has to be added to the environment as a secret variable.

        # Step 3: Configure aws credentials
        - name: Configure aws credentials
            uses: aws-actions/configure-aws-credentials@v2
            with:
                role-to-assume: ${{ secrets.AWS_PUT_DATA_ROLE}}
                aws-region: ${{ secrets.AWS_REGION }}

5. In the below Step 4 and Step 5 the job is installing python and setting up the environment variables that are later used by github-data-processor to process the data and put the data in AWS.The last step (Step 6) is where the required dependencies are installed and github-data-processor is ran to put the data to AWS. 

        # Step 4: Set up Python environment
        - name: Set up Python
            uses: actions/setup-python@v4
            with:
                python-version: '3.x'

        # Step 5: Set repository details as environment variable
        - name: Set ENV variable with repository name
            run: |
                echo "REPO_NAME=${{ github.repository }}" >> $GITHUB_ENV
                echo "REPO_PATH=${{ github.workspace }}" >> $GITHUB_ENV
                echo "REPO_URL=https://github.com/${{ github.repository }}" >> $GITHUB_ENV
                echo "BRANCH=${{ github.ref_name}}" >> $GITHUB_ENV
                echo "REPO_VISIBILITY=${{ github.event.repository.private }}" >> $GITHUB_ENV

        # Step 6: Run the github-data-processor project
        - name: Run scraper
            env:
                ROLE_ARN: ${{ secrets.AWS_PUT_DATA_ROLE }}
            run: |
                pip install -r github-data-processor/requirements.txt
                python github-data-processor/src/main.py  # This will run the github-data-processor project
