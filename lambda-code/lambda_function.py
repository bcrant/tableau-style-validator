import os
import json
from helpers import init_env
from download_workbook import download_workbook
from validate_styles import validate_styles


def lambda_handler(event, context):
    try:
        print('LAMBDA HANDLER event: ', event)

        init_env(event)

        # Get workbook
        tableau_workbook = download_workbook()

        # Get style guide
        with open(os.getenv('STYLE_GUIDE_PATH')) as sg:
            style_guide = json.load(sg)

        # Test workbook against style guide
        validate_styles(style_guide, tableau_workbook)

    except Exception as e:
        print(e)
        raise e


if __name__ == '__main__':
    if os.getenv('AWS_EXECUTION_ENV') is None:
        lambda_handler({}, {})
    else:
        print('i am a little teapot.')
