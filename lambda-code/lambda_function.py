import os
import sys
import json
from helpers import init_env
from tableau_download_twb import download_workbook
from validate_styles import validate_styles


def lambda_handler(event, context):
    print('LAMBDA HANDLER event: ', event)
    print('LAMBDA HANDLER context: ', context)

    init_env(event)

    print('os.environ: ', os.environ)
    print('os.getcwd: ', os.getcwd())
    print('sys.path: ', sys.path)

    # Get workbook
    tableau_workbook = download_workbook()

    # Get path to style guide
    sg_path = os.path.join(
        os.getenv('TABLEAU_PATH')
        + 'example_style_guide.json'
    )

    # Get style guide
    with open(sg_path) as sg:
        style_guide = json.load(sg)

    # Test workbook against style guide
    validate_styles(style_guide, tableau_workbook)

    return


if __name__ == '__main__':
    lambda_handler({}, {})
