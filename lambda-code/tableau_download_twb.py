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
        wb_file = server.workbooks.download(wb.id)
        #
        # with open(wb_file, 'wb') as f:
        zip = zipfile.ZipFile(wb_file)
        for z in zip.namelist():
            if '.twb' in z:
                print(z)
                zip.extract(z)
        zip.close()

            #         os.remove(workbook)
            #
            # # else file is twb
            # elif ct == "application/xml":
            #     with open(workbook, 'w') as file:
            #         file.write(response.text)
            #         file.close()




                    # with open(wb_file, 'r', encoding='ascii') as f:
        #     print(f.read())
            # f.write(wb_file)
            # print(f.encoding)
            # print(f.readable())
            # print(f.readlines())

        # with open('./wb.xml', "wb") as xml_file:
        #             xml_file.write(wb.workbook)

        # # Gets all workbook items
        # all_workbooks, pagination_item = server.workbooks.get()
        # print("\nThere are {} workbooks on site: ".format(pagination_item.total_available))
        # print([workbook.name for workbook in all_workbooks])
        #
        # if all_workbooks:
        #     # Pick one workbook from the list
        #     sample_workbook = all_workbooks[-1]
        #
        #     print(sample_workbook)

        # # Gets all webhook items
        # all_webhooks, pagination_item = server.webhooks.get()
        # print("\nThere are {} webhooks on site: ".format(pagination_item.total_available))
        # print([webhook for webhook in all_webhooks])
        #
        # if all_webhooks:
        #     # Pick one webhook from the list and delete it
        #     sample_webhook = all_webhooks[0]
        #     # sample_webhook.delete()
        #     print("+++" + sample_webhook.name)
        #
        #     print("Deleting webhook " + sample_webhook.name)
        #     server.webhooks.delete(sample_webhook.id)

    #     server.use_server_version()
    #     req_option = TSC.RequestOptions()
    #     print(req_option)

#         req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
#                                          TSC.RequestOptions.Operator.Equals, tabView))
#         all_views, pagination_item = server.views.get(req_option)
#         # Error catching for bad View names
#         if not all_views:
#             raise LookupError("View with the specified name was not found.")
#         view_item = all_views[0]
#         # Force refresh of screenshot if cached image more than one hour old
#         max_age = '1'
#         if not max_age:
#             max_age = '1'
#         image_req_option = TSC.ImageRequestOptions(imageresolution=TSC.ImageRequestOptions.Resolution.High,
#                                                    maxage=max_age)
#         server.views.populate_image(view_item, image_req_option)
#         # Save bytes as image
#         with open(tabPath, "wb") as image_file:
#             image_file.write(view_item.image)
#         print("Tableau image successfully saved to {0}".format(tabPath), '\n')
#
#
# def download(server, auth_token, site_id, workbook_id):
#     """
#     Downloads the desired workbook from the server (temp-file).
#
#     'server'        specified server address
#     'auth_token'    authentication token that grants user access to API calls
#     'site_id'       ID of the site that the user is signed into
#     'workbook_id'   ID of the workbook to download
#     Returns the filename of the workbook downloaded.
#     """
#     print("\tDownloading workbook to a temp file")
#     url = server + "/api/{0}/sites/{1}/workbooks/{2}/content".format(VERSION, site_id, workbook_id)
#     server_response = requests.get(url, headers={'x-tableau-auth': auth_token})
#     _check_status(server_response, 200)
#
#     # Header format: Content-Disposition: name="tableau_workbook"; filename="workbook-filename"
#     filename = re.findall(r'filename="(.*)"', server_response.headers['Content-Disposition'])[0]
#     with open(filename, 'wb') as f:
#         f.write(server_response.content)
#     return filename


if __name__ == "__main__":
    authenticate_tableau()
