import os
import json
from dotenv import load_dotenv
from tableau_download_twb import download_workbook
from validate_styles import validate_styles


def init_env():
    # Determine whether running in Lambda or locally
    if os.getenv('AWS_EXECUTION_ENV') is None:
        print('Operating in local dev context, loading ./envs/.env file...')
        load_dotenv('./envs/.env')
    else:
        print('Operating in Lambda context...')


def lambda_handler(event, context):
    print(event)
    print(context)

    init_env()

    # Get workbook
    tableau_workbook = download_workbook()

    # Get style guide
    with open('./tests/sg_example.json') as sg:
        style_guide = json.load(sg)

    # Test workbook and style guide
    validate_styles(style_guide, tableau_workbook)

    return


if __name__ == '__main__':
    lambda_handler({}, {})
