# Tableau Style Validator Setup
All instructions assume macOS, that you have [Homebrew](https://brew.sh/) and `git` installed, and tries not to assume anything else. Let me know if I overlooked anything or if you run into any troubles getting set up using these instructions.


### Cloud Deployment Overview
Before diving into the specifics, let's take a look at the project architecture...  

![Tableau Style Validator Architecture](./images/TableauStyleValidatorArchitecture.png)

# Prerequisites
### Third Party Accounts
In addition to Tableau Server / Tableau Online, we will be using several web technologies that will require you to create new accounts or access accounts for which you have admin privileges.
- Amazon Web Services
- Slack
- Zapier

### Are these services free?
This project can run entirely within free tier AWS service quotas and free tier Slack workspace. Zapier offers a free trial, but would require a paid subscription for a production deployment.

Side Note: if you are deploying this to production, you may consider setting up a [Virtual Private Cloud](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html) through which your Lambda function can access the internet.
By default, Lambda runs your functions in a secure VPC with access to AWS services and the internet. However secure that may be, depending on what kind of data you are working with and what SLAs are in place, you may need to deviate from Lambda's default configuration. 

Another option would be to configure an [Internet Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html) or route an existing [NAT Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) that has internet access. Either of these solutions can be implemented in a few ways:
1. Call DevOps
2. Call DevOps
3. Call DevOps

I mention all of this only because both AWS VPC and AWS Internet Gateways are paid services.  
/rant

### Credentials
Following the steps below will give you access to all the credentials that you will need for this project. If you have some of these accounts and are not sure if you have all the credentials, you can view the [example.env](../cloud-deployment/envs/example.env) for a full list of the credentials you will need. 

If you are not familiar with environment variables, hidden files like `.env` and the Python `dotenv` package, you can visit [this document](https://github.com/bcrant/Tableau2Slack/blob/main/documentation/2-virtualenvexample.md#environment-variables) for a crash course.

### Create a copy of the [example.env](../cloud-deployment/envs/example.env) and name it `.env`.

You will be replacing the sample values with your credentials and desired variable names as you complete the next steps.

# Third Party Setup & Configuration
### AWS steps…
This will be the slowest part, so we'll knock it out first. A bit later we will be running the [build scripts](../cloud-deployment/scripts) which abstract away most of the deployment. We just have to create those resources first.
          
- Make account or log in
- Look at [example.env](../cloud-deployment/envs/example.env) to get a preview of the credentials you will need / be producing
- Make an S3 Bucket
- Make a Lambda function
    - Select the `Python 3.8 runtime` for the function's base image
- Create an AWS IAM Execution Role
    - Open the roles page in the IAM console
    - Choose "Create role"
    - Create a role with the following properties
      - Trusted entity – `Lambda`
      - Permissions – `AWSLambdaVPCAccessExecutionRole`
      - Role name – `lambda-vpc-role`
- Add your AWS credentials and variable names to your `.env` file

### Zapier steps…
- Make account or log in
- Requires a paid “Premium Connection” (AWS Lambda)
- Start a free 7-day trial to test
- Create a new “Zap”
- Trigger: 1. Catch Hook
    - Add “Custom Webhook URL” to your `.env`
    - Test Trigger 
        - Requires you to already have the webhooks installed on your server
        - You can do this by running the [download_workbook.py](../lib/download_workbook.py) script
        - Alternatively, if you prefer having a UI, you could use Postman and follow the [Tableau Webhook tutorial](https://github.com/tableau/webhooks-docs)
- Action: 2. Invoke Function in AWS Lambda
    - You will need to have made the (AWS account) and Lambda function
    - Select your function from UI
    - For the arguments we want to pass to Lambda, select `RESOURCE_LUID`
    
You should now have something that looks like...
![Zapier Config](images/zapier_zap.png)
 

### Slack steps…
- Make workspace or log in
- Create a new [Slack App for your workspace](https://api.slack.com/apps)
- Go to OAuth & Permissions —> Scopes —> Bot Token Scopes
- Add an OAuth Scope…
    - `chat:write`
    - `chat:write.customize`
- Install your Slack Bot to your workspace.
- Add your Slack environment variables to `.env`
    - Add the Slack Bot User OAuth Access Token to `.env`
    - Add the channel you want to post to in `.env`
- IMPORTANT: Add the Slack bot to the channel you will be posting to by running this Slack command in that channel: `/invite @BOT_NAME`


# Python Environment
### 1. Clone Repository
- `$ mkdir tableau-style-validator`
- `$ cd tableau-style-validator`
- `$ git clone https://github.com/bcrant/tableau-style-validator.git` 

### 2. Prepare Python
Install the Python version manager `pyenv`
- `$ brew install pyenv`
- `$ brew install pyenv-virtualenv`
  
Download the Python version used in this project.
- `$ pyenv install 3.8.10`
- `$ pyvenv local 3.8.10`

Create a virtual environment for this project using that Python version.
- `$ pyenv virtualenv 3.8.10 tableau_style_validator`
- `$ pip install --upgrade pip`
- `$ pip install -r requirements-cli.txt`

Install the build dependencies to your virtual environment (mainly AWS CLI)
- `$ cd cloud-deployment && pip install -r ./requirements-aws-env.txt`

You will then need to [configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) with your credentials
- `$ aws configure`

I've gone ahead and uploaded the dependencies that your Lambda Function needs to [validator-deps.zip](../cloud-deployment/lambda-deps/validator-deps.zip). If you do not wish to use Docker, you _could_ upload that zip to a new Lambda Layer and edit the [2.code-build.sh](../cloud-deployment/scripts/2.code-build.sh) (remove the `docker run` line but keep its arguments).

### 3. Prepare Docker
 - Visit https://hub.docker.com/editions/community/docker-ce-desktop-mac/ and download the Docker.dmg.
 - Install & Run Docker.dmg
 - Make sure the docker whale is running in the system bar.


# Deploying the Project