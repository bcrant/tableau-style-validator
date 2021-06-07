# Tableau Style Validator Setup
All instructions assume MacOS.

The below steps create an isolated Python environment to quickly test the program from your command line, and assumes to prior Python knowledge/ experience. 

Afterwards, we will go in depth walking through the serverless deployment, hosted on all free tier AWS products.

## Prepare Docker
 - Visit https://hub.docker.com/editions/community/docker-ce-desktop-mac/ and download the Docker.dmg.
 - Install & Run Docker.dmg
 - Make sure the docker whale is running in the system bar.

## Prepare Python
Creating a virtual env is optional.
- `brew install pyenv`
- `pyenv install 3.8.10`
- `pyvenv global 3.8.10`
- `pyenv virtualenv 3.8.10 tableau_style_validator`
    - (also requires `brew install pyenv-virtualenv`)
- `pip install --upgrade pip`   
(Get AWS deps native to AWS Lambda Linux Server for local use)
- `cd pipeline && pip install -r ./requirements-aws-env.txt`   
(Get deps served as Lambda Layer in remote for local use)
- `cd lambda-deps && pip install -r ./requirements-deps.txt`
## Setup IAM Execution Role
To create an execution role.
* Open the roles page in the IAM console.
* Choose Create role.
* Create a role with the following properties.
  * Trusted entity – `Lambda`.
  * Permissions – `AWSLambdaVPCAccessExecutionRole`.
  * Role name – `lambda-vpc-role`.
