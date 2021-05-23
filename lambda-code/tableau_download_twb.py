import os
import zipfile
from dotenv import load_dotenv
import tableauserverclient as TSC


def init_env():
    if os.getenv('AWS_EXECUTION_ENV') is None:
        print('Operating in local dev context, loading ./envs/.env file...')
        load_dotenv('./envs/.env')
    else:
        print('Operating in Lambda context...')


def download_workbook():
    init_env()
    #
    # Import Tableau environment variables
    # For further explanation of Tableau environment variables visit:
    # https://tableau.github.io/server-client-python/docs/api-ref#tableauauth-class
    #                                               # EXAMPLE VALUES:
    USERNAME = os.getenv('TABLEAU_USER')            # you@email.com
    PASS = os.getenv('TABLEAU_PASS')                # password
    SITE_NAME = os.getenv('TABLEAU_SITE_NAME')      # site-name AKA content-url
    SERVER_URL = os.getenv('TABLEAU_SERVER_URL')    # https://10ay.online.tableau.com

    # (For local testing... will need to get this from the Zapier Webhook invocation JSON Payload)
    TABLEAU_RESOURCE_LUID = os.getenv('RESOURCE_LUID')

    print("Signing into Tableau Server and fetching Workbook...")
    tableau_auth = TSC.TableauAuth(USERNAME, PASS, SITE_NAME)
    server = TSC.Server(SERVER_URL)
    server.use_server_version()

    with server.auth.sign_in(tableau_auth):
        # Select specific workbook with Resource LUID from Webhook payload
        wb = server.workbooks.get_by_id(TABLEAU_RESOURCE_LUID)

        print(f'Downloading "{wb.name}" from Tableau Server')
        zipped_wb_path = server.workbooks.download(wb.id, include_extract=True)

        # .twbx files are zipped archives. Here we extract the Workbook (.twb) only.
        unzipped_wb_path = None
        with zipfile.ZipFile(zipped_wb_path) as packaged_workbook:
            for wb_file in packaged_workbook.namelist():
                if '.twb' in wb_file:
                    unzipped_wb_path = packaged_workbook.extract(wb_file)
                    print(f'Extracting "{wb_file}" from {wb.name}.')
                else:
                    print(f'No Tableau Workbook file found in {wb.name}')

        # Pass Tableau Workbook to parser as open file
        with open(unzipped_wb_path) as f:
            wb_f = f.read()

        return wb_f


if __name__ == "__main__":
    download_workbook()
