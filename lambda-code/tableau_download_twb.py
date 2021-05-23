import os
import zipfile
import requests
from io import StringIO, BytesIO
from dotenv import load_dotenv
import tableauserverclient as TSC

#
# Call this script with payload of Tableau Webhook
# Sample Payload:
#
# site_luid   f6a2b550-8b37-45c3-957e-99702e3dc5f6
# resource    WORKBOOK
# resource_luid   e03412ce-ab0f-4ca2-8ce8-fa9976737a68
# resource_name   TestWebhook
# event_type  WorkbookCreated
# created_at  2021-05-21T04:12:08.662Z


def init_env():
    if os.getenv('AWS_EXECUTION_ENV') is None:
        print('Operating in local/dev context, loading ../.env file...')
        load_dotenv('./envs/.env')
    else:
        print('Operating in Lambda context...')


def _encode_for_display(text):
    """
    Encodes strings so they can display as ASCII in a Windows terminal window.
    This function also encodes strings for processing by xml.etree.ElementTree functions.
    Returns an ASCII-encoded version of the text.
    Unicode characters are converted to ASCII placeholders (for example, "?").
    """
    return text.encode('ascii', errors="backslashreplace").decode('utf-8')


def authenticate_tableau():
    init_env()

    # Import Tableau environment variables          # EXAMPLE VALUES:
    USERNAME = os.getenv('TABLEAU_USER')
    PASS = os.getenv('TABLEAU_PASS')
    SITE_NAME = os.getenv('TABLEAU_SITE_NAME')      # site-name AKA content-url
    SERVER_URL = os.getenv('TABLEAU_SERVER_URL')    # https://10ay.online.tableau.com
    # For further explanation of Tableau environment variables visit:
    # https://tableau.github.io/server-client-python/docs/api-ref#tableauauth-class

    # (For local testing... will need to get these from the Zapier Webhook invocation JSON Payload)
    TABLEAU_SITE_LUID = os.getenv('SITE_LUID')
    TABLEAU_RESOURCE_LUID = os.getenv('RESOURCE_LUID')

    print("Talking to Tableau...\n")
    tableau_auth = TSC.TableauAuth(USERNAME, PASS, SITE_NAME)
    print(tableau_auth)
    server = TSC.Server(SERVER_URL)
    print(server)

    server.use_server_version()
    print(server.version)

    # Signing into Tableau Server and fetching Workbook
    with server.auth.sign_in(tableau_auth):

        # Select specific workbook with Resource LUID from Webhook payload
        wb = server.workbooks.get_by_id(TABLEAU_RESOURCE_LUID)

        print(f'Downloading {wb.name} from {SERVER_URL}/{SITE_NAME}')
        wb_file = server.workbooks.download(wb.id, include_extract=False)

        # Files download as twbx in zipped form...
        print(wb_file)
        zipped_twbx = zipfile.ZipFile(wb_file)
        print(zipped_twbx.namelist())
        print(zipped_twbx.infolist())

        for z in zipped_twbx.namelist():
            print(z)
            if '.twb' in z:
                print(z)
        #         zipped_twbx.extract(z)
        # zipped_twbx.close()


if __name__ == "__main__":
    authenticate_tableau()
