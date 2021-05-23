import os
from tableau_download_twb import download_workbook


def lambda_handler(event, context):
    print(event)
    print(context)

    # Determine whether running in Lambda or locally
    download_workbook()

    return
