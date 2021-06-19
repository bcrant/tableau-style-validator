# Tableau Style Validator Setup
The below steps create an isolated Python environment to quickly test the program from your command line, and assumes to prior Python knowledge/ experience. 

Afterwards, we will go in depth walking through the serverless deployment, hosted on all free tier AWS products.

# Quick Start

All instructions assume MacOS and that you have [Homebrew](https://brew.sh/) and `git` installed and tries not to assume anything else. 

Let me know if I overlooked anything or if you run into any troubles getting set up using these instructions.

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

### 3. Run Demo

That's it! You can now run `validator_cli.py` using the example Style Guide and Workbook in the ["tests" directory](../tests/) of this repository using this command:

`$ python validator_cli.py -s ./tests/example_style_guide.json -w ./tests/example_workbook.twb`

Here is a screenshot of the expected output of this command for reference...
![CLI Output](./images/CLI_Output.png)




# Cloud Deployment
(Get AWS deps native to AWS Lambda Linux Server for local use)
- `cd cloud-deployment && pip install -r ./requirements-aws-env.txt`

(Get deps served as Lambda Layer in remote for local use)
- `cd lambda-deps && pip install -r ./requirements-deps.txt`


## Prepare Docker
 - Visit https://hub.docker.com/editions/community/docker-ce-desktop-mac/ and download the Docker.dmg.
 - Install & Run Docker.dmg
 - Make sure the docker whale is running in the system bar.

## Setup IAM Execution Role
To create an execution role...
* Open the roles page in the IAM console.
* Choose Create role.
* Create a role with the following properties.
  * Trusted entity – `Lambda`.
  * Permissions – `AWSLambdaVPCAccessExecutionRole`.
  * Role name – `lambda-vpc-role`.
