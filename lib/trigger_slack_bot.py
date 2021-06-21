import os
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


#
# Trigger Slack Bot
#
def trigger_slack_bot(workbook_output, dashboard_output, worksheet_output):
    try:
        # Connect to Slack
        print("Authenticating Slack Bot...")
        slack_client = WebClient(token=os.getenv('SLACK_TOKEN'))

        # Construct "builder" and "attachments" json payloads.
        print("Preparing message...")
        blocks_json = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "{}".format('\n\n')
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Validating top-level WORKBOOK styles...{}".format(workbook_output)
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Validating each DASHBOARD in workbook...{}".format(dashboard_output)
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Validating each WORKSHEET in workbook...{}".format(worksheet_output)
                }
            }
        ]

        print("Sending message...")
        response = slack_client.chat_postMessage(
            channel=os.getenv('SLACK_CHANNEL'),
            icon_url='https://briancrant.com/wp-content/uploads/2021/05/magnifyingglass.jpg',
            username='Tableau Style Validator',
            blocks=json.dumps(blocks_json),
            text='A workbook has been created/updated. See validation results...'
        )

        print("Finished posting message to Slack. Goodbye.")

        # Out of the box Slack error handling
    except SlackApiError as e:
        assert e.response['ok'] is False
        assert e.response['error']
        print(f'Got an error: {e.response["error"]}')
