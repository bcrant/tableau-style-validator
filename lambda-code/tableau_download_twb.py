import os
import zipfile
import tableauserverclient as TSC


def download_workbook():
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

    print('Signing into Tableau Server...')
    tableau_auth = TSC.TableauAuth(USERNAME, PASS, SITE_NAME)
    server = TSC.Server(SERVER_URL)
    server.use_server_version()

    with server.auth.sign_in(tableau_auth):
        #
        # Before downloading workbook, make sure correct webhooks are installed
        #
        hooks = server.webhooks.get()

        print('Checking for webhooks and installing if they do not exist...')
        if check_webhooks_for_wb_created(hooks) is not True:
            create_webhook_for_wb_created(server)

        if check_webhooks_for_wb_updated(hooks) is not True:
            create_webhook_for_wb_updated(server)

        #
        # Select specific workbook with Resource LUID from Webhook payload
        #
        wb = server.workbooks.get_by_id(TABLEAU_RESOURCE_LUID)

        print(f'Downloading "{wb.name}" from Tableau Server...')
        zipped_wb_path = server.workbooks.download(wb.id, filepath='./lambda-code/', include_extract=True)

        # Packaged Workbook (.twbx) files are zipped archives. Here we extract the Workbook (.twb) only.
        unzipped_wb_path = None
        with zipfile.ZipFile(zipped_wb_path) as packaged_workbook:
            for wb_file in packaged_workbook.namelist():
                if '.twb' in wb_file:
                    unzipped_wb_path = packaged_workbook.extract(wb_file, './lambda-code/')
                    print(f'Extracting "{wb_file}" from "{wb.name}"...')
                else:
                    print(f'No Tableau Workbook file found in "{wb.name}".')

        # Pass Tableau Workbook to parser as open file
        with open(unzipped_wb_path) as f:
            wb_f = f.read()

        return wb_f


def check_webhooks_for_wb_created(tsc_webhook_items):
    if tsc_webhook_items is not None:
        for hook in tsc_webhook_items[0]:
            if 'workbook-created' in hook.event:
                print(f'Found webhook "{hook.name}" on Tableau Server for "{hook.event}" event.')
                return True


def create_webhook_for_wb_created(tsc_server_obj):
    # Create webhook for Workbook Created events
    c_webhook = TSC.WebhookItem()
    c_webhook.name = os.getenv('WB_CREATED_WEBHOOK_NAME')
    c_webhook.event = os.getenv('WB_CREATED_WEBHOOK_EVENT')
    c_webhook.url = os.getenv('TABLEAU_WEBHOOK_URL')
    c_webhook = tsc_server_obj.webhooks.create(c_webhook)
    print('Installed missing webhook for workbook-created event. Webhook ID: {}'.format(c_webhook.id))


def check_webhooks_for_wb_updated(tsc_webhook_items):
    if tsc_webhook_items is not None:
        for hook in tsc_webhook_items[0]:
            if 'workbook-updated' in hook.event:
                print(f'Found webhook "{hook.name}" on Tableau Server for "{hook.event}" event.')
                return True


def create_webhook_for_wb_updated(tsc_server_obj):
    # Create webhook for Workbook Updated events
    u_webhook = TSC.WebhookItem()
    u_webhook.name = os.getenv('WB_UPDATED_WEBHOOK_NAME')
    u_webhook.event = os.getenv('WB_UPDATED_WEBHOOK_EVENT')
    u_webhook.url = os.getenv('TABLEAU_WEBHOOK_URL')
    u_webhook = tsc_server_obj.webhooks.create(u_webhook)
    print('Installed missing webhook for workbook-updated event. Webhook ID: {}'.format(u_webhook.id))


if __name__ == "__main__":
    download_workbook()
