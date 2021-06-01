import os
import json
from textwrap import dedent
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from parse_xml import get_tableau_styles
from helpers import left_align_list
from alerts_local_fmt import PrintAlerts, msg, err_msg
from alerts_slack_fmt import SlackAlerts, slack_msg, slack_err_msg


def validate_styles(style_guide_json, workbook_file):
    #
    # Parse styles from Tableau Workbook file
    #
    styles = get_tableau_styles(workbook_file)

    # Workbook styles
    wb_styles = styles.get('workbook_styles')
    wb_response = test_workbook(wb_styles, style_guide_json)

    # Dashboard styles
    db_styles = styles.get('dashboard_styles')
    db_response = test_dashboards(db_styles, style_guide_json)

    # Worksheet styles
    ws_styles = styles.get('worksheet_styles')
    ws_response = test_worksheets(ws_styles, style_guide_json)

    #
    # Trigger Slack Bot to send a formatted message
    #
    if os.getenv('AWS_EXECUTION_ENV') is not None:
        try:
            # Connect to Slack
            print("Authenticating Slack Bot...")
            slack_client = WebClient(token=os.getenv('SLACK_TOKEN'))

            # Construct "builder" and "attachments" json payloads.
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
                        "text": "Validating top-level WORKBOOK styles...{}".format(wb_response)
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Validating each DASHBOARD in workbook...{}".format(db_response)
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Validating each WORKSHEET in workbook...{}".format(ws_response)
                    }
                }
            ]

            response = slack_client.chat_postMessage(
                channel=os.getenv('SLACK_CHANNEL'),
                icon_url='https://briancrant.com/wp-content/uploads/2021/05/magnifyingglass.jpg',
                username='Tableau Style Validator',
                blocks=json.dumps(blocks_json),
                text='A workbook has been created/updated. See validation results...'
            )

            # Out of the box Slack error handling
        except SlackApiError as e:
            assert e.response['ok'] is False
            assert e.response['error']
            print(f'Got an error: {e.response["error"]}')

    return


#
# WORKBOOK
#
def test_workbook(workbook_styles, sg):
    # print('Workbook Styles at time of testing:\n', pp(workbook_styles))
    print(dedent('''
    
        Validating all top-level WORKBOOK styles...
        '''))

    valid_wb_styles_list = []
    invalid_wb_styles_list = []
    wb_err_count = 0

    for item in workbook_styles:
        styles = workbook_styles.get(item)
        # #
        # # Test all colors in workbook before specific styles
        # # (Excluding until later iterations)
        # #
        # if 'all_colors_in_wb' in item:
        #     for hex_code in styles:
        #         if hex_code.upper() not in sg.get('all-colors') + sg.get('font-colors') + sg.get('background-colors'):
        #             print(hex_code.upper())

        #
        # Test all workbook level font styles
        #
        if isinstance(styles, dict):
            for style in styles:
                s = styles.get(style)
                if s is not None:
                    if 'font-size' in style:
                        if s not in sg.get('font-sizes'):
                            invalid_wb_styles_list.append(
                                slack_msg(SlackAlerts.INVALID_FONT_SIZE,
                                          s,
                                          item,
                                          valid=False,
                                          kind='font-size',
                                          level='Workbook')
                            )

                            msg(PrintAlerts.INVALID_FONT_SIZE,
                                s,
                                item,
                                valid=False,
                                kind='font-size',
                                level='Workbook')
                            wb_err_count += 1
                        else:
                            valid_wb_styles_list.append(
                                slack_msg(SlackAlerts.VALID_FONT_SIZE,
                                          s,
                                          item,
                                          valid=True,
                                          kind='font-size',
                                          level='Workbook')
                            )

                            msg(PrintAlerts.VALID_FONT_SIZE,
                                s,
                                item,
                                valid=True,
                                kind='font-size',
                                level='Workbook')

                    if 'font-family' in style:
                        if s not in sg.get('fonts'):
                            invalid_wb_styles_list.append(
                                slack_msg(SlackAlerts.INVALID_FONT_TYPE,
                                          s,
                                          item,
                                          valid=False,
                                          kind='font-type',
                                          level='Workbook')
                            )

                            msg(PrintAlerts.INVALID_FONT_TYPE,
                                s,
                                item,
                                valid=False,
                                kind='font-type',
                                level='Workbook')
                            wb_err_count += 1
                        else:
                            valid_wb_styles_list.append(
                                slack_msg(SlackAlerts.INVALID_FONT_TYPE,
                                          s,
                                          item,
                                          valid=True,
                                          kind='font-type',
                                          level='Workbook')
                            )

                            msg(PrintAlerts.VALID_FONT_TYPE,
                                s,
                                item,
                                valid=True,
                                kind='font-type',
                                level='Workbook')

                    if 'color' in style:
                        if s.upper() not in sg.get('font-colors'):
                            invalid_wb_styles_list.append(
                                slack_msg(SlackAlerts.INVALID_FONT_COLOR,
                                          s,
                                          item,
                                          valid=False,
                                          kind='font-color',
                                          level='Workbook'))

                            msg(PrintAlerts.INVALID_FONT_COLOR,
                                s.upper(),
                                item,
                                valid=False,
                                kind='font-color',
                                level='Workbook')
                            wb_err_count += 1
                        else:
                            valid_wb_styles_list.append(
                                slack_msg(SlackAlerts.VALID_FONT_COLOR,
                                          s,
                                          item,
                                          valid=True,
                                          kind='font-color',
                                          level='Workbook'))

                            msg(PrintAlerts.VALID_FONT_COLOR,
                                s.upper(),
                                item,
                                valid=True,
                                kind='font-color',
                                level='Workbook')

    err_msg(wb_err_count)

    if wb_err_count == 0:
        valid_wb_styles_list.append(
            slack_err_msg(wb_err_count)
        )
    else:
        invalid_wb_styles_list.append(
            slack_err_msg(wb_err_count)
        )

    return dedent('''
    
Invalid Styles: {invalid}
                
Valid Styles: {valid}

'''.format(invalid=left_align_list(invalid_wb_styles_list) if invalid_wb_styles_list else None,
           valid=left_align_list(valid_wb_styles_list) if valid_wb_styles_list else None))


#
# DASHBOARDS
#
def test_dashboards(dashboard_styles, sg):
    # print('Dashboard Styles at time of testing:\n', pp(dashboard_styles))
    print(dedent('''

    Validating each DASHBOARD in workbook...
    '''))

    valid_db_styles_list = []
    invalid_db_styles_list = []
    db_err_count = 0
    for dashboard in dashboard_styles:
        dashboard_style = dashboard_styles.get(dashboard)
        db_name = dashboard_style.get('db_name')
        for item in dashboard_style:
            styles = dashboard_style.get(item)
            if isinstance(styles, dict):
                for style in styles:
                    s = styles.get(style)
                    if s is not None:
                        if 'font-size' in style:
                            if s not in sg.get('font-sizes'):
                                invalid_db_styles_list.append(
                                    slack_msg(SlackAlerts.INVALID_FONT_SIZE,
                                              s,
                                              item,
                                              valid=False,
                                              kind='font-size',
                                              level=db_name))

                                msg(PrintAlerts.INVALID_FONT_SIZE,
                                    s,
                                    item,
                                    valid=False,
                                    kind='font-size',
                                    level=db_name)
                                db_err_count += 1
                            else:
                                valid_db_styles_list.append(
                                    slack_msg(SlackAlerts.VALID_FONT_SIZE,
                                              s,
                                              item,
                                              valid=True,
                                              kind='font-size',
                                              level=db_name))

                                msg(PrintAlerts.VALID_FONT_SIZE,
                                    s,
                                    item,
                                    valid=True,
                                    kind='font-size',
                                    level=db_name)

                        if 'font-family' in style:
                            if s not in sg.get('fonts'):
                                invalid_db_styles_list.append(
                                    slack_msg(SlackAlerts.INVALID_FONT_TYPE,
                                              s,
                                              item,
                                              valid=False,
                                              kind='font-type',
                                              level=db_name))

                                msg(PrintAlerts.INVALID_FONT_TYPE,
                                    s,
                                    item,
                                    valid=False,
                                    kind='font-type',
                                    level=db_name)
                                db_err_count += 1
                            else:
                                valid_db_styles_list.append(
                                    slack_msg(SlackAlerts.INVALID_FONT_TYPE,
                                              s,
                                              item,
                                              valid=True,
                                              kind='font-type',
                                              level=db_name))

                                msg(PrintAlerts.VALID_FONT_TYPE,
                                    s,
                                    item,
                                    valid=True,
                                    kind='font-type',
                                    level=db_name)

                        # This excludes dashboard zone styles (background color, border colors) to only get font color.
                        if 'db_zone_styles' not in item:
                            if 'color' in style:
                                if s.upper() not in sg.get('font-colors'):
                                    invalid_db_styles_list.append(
                                        slack_msg(SlackAlerts.INVALID_FONT_COLOR,
                                                  s,
                                                  item,
                                                  valid=False,
                                                  kind='font-color',
                                                  level=db_name))

                                    msg(PrintAlerts.INVALID_FONT_COLOR,
                                        s.upper(),
                                        item,
                                        valid=False,
                                        kind='font-color',
                                        level=db_name)
                                    db_err_count += 1
                                else:
                                    valid_db_styles_list.append(
                                        slack_msg(SlackAlerts.INVALID_FONT_COLOR,
                                                  s,
                                                  item,
                                                  valid=True,
                                                  kind='font-color',
                                                  level=db_name))

                                    msg(PrintAlerts.VALID_FONT_COLOR,
                                        s.upper(),
                                        item,
                                        valid=True,
                                        kind='font-color',
                                        level=db_name)
                        #
                        # Dashboard Zone styles
                        #
                        # NOTE: if you do not wish to test margins, padding, etc...
                        # you can comment out this entire else clause.
                        else:
                            # Convert any singular string items to list before validating as lists
                            if isinstance(s, str):
                                s = list(s)
                            for val in s:
                                if 'border-color' in style:
                                    if val.upper() not in sg.get('border-colors'):
                                        msg(PrintAlerts.INVALID_BORDER_COLOR,
                                            val.upper(),
                                            item,
                                            valid=False,
                                            kind='border-color',
                                            level=db_name)
                                        db_err_count += 1
                                    else:
                                        msg(PrintAlerts.VALID_BORDER_COLOR,
                                            val.upper(),
                                            item,
                                            valid=True,
                                            kind='border-color',
                                            level=db_name)

                                if 'border-width' in style:
                                    if val not in sg.get('border-width'):
                                        msg(PrintAlerts.INVALID_BORDER_COLOR,
                                            val,
                                            item,
                                            valid=False,
                                            kind='border-width',
                                            level=db_name)
                                        db_err_count += 1
                                    else:
                                        msg(PrintAlerts.VALID_BORDER_COLOR,
                                            val,
                                            item,
                                            valid=True,
                                            kind='border-width',
                                            level=db_name)

                                if 'border-style' in style:
                                    if val not in sg.get('border-style'):
                                        msg(PrintAlerts.INVALID_BORDER_STYLE,
                                            val,
                                            item,
                                            valid=False,
                                            kind='border-style',
                                            level=db_name)
                                        db_err_count += 1
                                    else:
                                        msg(PrintAlerts.VALID_BORDER_STYLE,
                                            val,
                                            item,
                                            valid=True,
                                            kind='border-style',
                                            level=db_name)

                                if 'margin' in style:
                                    if val not in sg.get('margin'):
                                        msg(PrintAlerts.INVALID_MARGIN,
                                            val,
                                            item,
                                            valid=False,
                                            kind='margin',
                                            level=db_name)
                                        db_err_count += 1
                                    else:
                                        msg(PrintAlerts.VALID_MARGIN,
                                            val,
                                            item,
                                            valid=True,
                                            kind='margin',
                                            level=db_name)

                                if 'margin-top' in style:
                                    if val not in sg.get('margin-top'):
                                        msg(PrintAlerts.INVALID_MARGIN_TOP,
                                            val,
                                            item,
                                            valid=False,
                                            kind='margin-top',
                                            level=db_name)
                                        db_err_count += 1
                                    else:
                                        msg(PrintAlerts.VALID_MARGIN_TOP,
                                            val,
                                            item,
                                            valid=True,
                                            kind='margin-top',
                                            level=db_name)

                                if 'margin-bottom' in style:
                                    if val not in sg.get('margin-bottom'):
                                        msg(PrintAlerts.INVALID_MARGIN_BOTTOM,
                                            val,
                                            item,
                                            valid=False,
                                            kind='margin-bottom',
                                            level=db_name)
                                        db_err_count += 1
                                    else:
                                        msg(PrintAlerts.VALID_MARGIN_BOTTOM,
                                            val,
                                            item,
                                            valid=True,
                                            kind='margin-bottom',
                                            level=db_name)

                                if 'background-color' in style:
                                    if val.upper() not in sg.get('background-colors'):
                                        msg(PrintAlerts.INVALID_BACKGROUND_COLOR,
                                            val.upper(),
                                            item,
                                            valid=False,
                                            kind='bg-color',
                                            level=db_name)
                                        db_err_count += 1
                                    else:
                                        msg(PrintAlerts.VALID_BACKGROUND_COLOR,
                                            val.upper(),
                                            item,
                                            valid=True,
                                            kind='bg-color',
                                            level=db_name)

                                if 'padding' in style:
                                    if val not in sg.get('padding'):
                                        msg(PrintAlerts.INVALID_PADDING,
                                            val,
                                            item,
                                            valid=False,
                                            kind='padding',
                                            level=db_name)
                                        db_err_count += 1
                                    else:
                                        msg(PrintAlerts.VALID_PADDING,
                                            val,
                                            item,
                                            valid=True,
                                            kind='padding',
                                            level=db_name)

    err_msg(db_err_count)

    if db_err_count == 0:
        valid_db_styles_list.append(
            slack_err_msg(db_err_count)
        )
    else:
        invalid_db_styles_list.append(
            slack_err_msg(db_err_count)
        )

    return dedent('''

Invalid Styles: {invalid}


Valid Styles: {valid}

'''.format(invalid=left_align_list(invalid_db_styles_list) if invalid_db_styles_list else None,
           valid=left_align_list(valid_db_styles_list) if valid_db_styles_list else None))


#
# WORKSHEETS
#
def test_worksheets(worksheet_styles, sg):
    # print('Worksheet Styles at time of testing:\n', pp(worksheet_styles))
    print(dedent('''

    Validating each WORKSHEET in workbook...
    '''))

    valid_ws_styles_list = []
    invalid_ws_styles_list = []
    ws_err_count = 0
    for worksheet_style in worksheet_styles:
        worksheet = worksheet_styles.get(worksheet_style)
        ws_name = worksheet_style
        for item in worksheet:
            styles = worksheet.get(item)
            for style_dict in styles:
                if isinstance(style_dict, dict):
                    for style in style_dict:
                        s = style_dict.get(style)
                        if s is not None:
                            if 'fontsize' in style:
                                if s not in sg.get('font-sizes'):
                                    invalid_ws_styles_list.append(
                                        slack_msg(SlackAlerts.INVALID_FONT_SIZE,
                                                  s,
                                                  item,
                                                  valid=False,
                                                  kind='font-size',
                                                  level=ws_name))

                                    msg(PrintAlerts.INVALID_FONT_SIZE,
                                        s,
                                        item,
                                        valid=False,
                                        kind='font-size',
                                        level=ws_name)
                                    ws_err_count += 1
                                else:
                                    valid_ws_styles_list.append(
                                        slack_msg(SlackAlerts.VALID_FONT_SIZE,
                                                  s,
                                                  item,
                                                  valid=True,
                                                  kind='font-size',
                                                  level=ws_name))

                                    msg(PrintAlerts.VALID_FONT_SIZE,
                                        s,
                                        item,
                                        valid=True,
                                        kind='font-size',
                                        level=ws_name)

                            if 'fontname' in style:
                                if s not in sg.get('fonts'):
                                    invalid_ws_styles_list.append(
                                        slack_msg(SlackAlerts.INVALID_FONT_TYPE,
                                                  s,
                                                  item,
                                                  valid=False,
                                                  kind='font-name',
                                                  level=ws_name))

                                    msg(PrintAlerts.INVALID_FONT_TYPE,
                                        s,
                                        item,
                                        valid=False,
                                        kind='font-name',
                                        level=ws_name)
                                    ws_err_count += 1
                                else:
                                    valid_ws_styles_list.append(
                                        slack_msg(SlackAlerts.VALID_FONT_TYPE,
                                                  s,
                                                  item,
                                                  valid=True,
                                                  kind='font-name',
                                                  level=ws_name))

                                    msg(PrintAlerts.VALID_FONT_TYPE,
                                        s,
                                        item,
                                        valid=True,
                                        kind='font-name',
                                        level=ws_name)

                            if 'fontcolor' in style:
                                if s.upper() not in sg.get('font-colors'):
                                    invalid_ws_styles_list.append(
                                        slack_msg(SlackAlerts.INVALID_FONT_COLOR,
                                                  s,
                                                  item,
                                                  valid=False,
                                                  kind='font-color',
                                                  level=ws_name))

                                    msg(PrintAlerts.INVALID_FONT_COLOR,
                                        s.upper(),
                                        item,
                                        valid=False,
                                        kind='font-color',
                                        level=ws_name)
                                    ws_err_count += 1
                                else:
                                    valid_ws_styles_list.append(
                                        slack_msg(SlackAlerts.VALID_FONT_SIZE,
                                                  s,
                                                  item,
                                                  valid=True,
                                                  kind='font-color',
                                                  level=ws_name))

                                    msg(PrintAlerts.VALID_FONT_COLOR,
                                        s.upper(),
                                        item,
                                        valid=True,
                                        kind='font-color',
                                        level=ws_name)

    err_msg(ws_err_count)

    if ws_err_count == 0:
        valid_ws_styles_list.append(
            slack_err_msg(ws_err_count)
        )
    else:
        invalid_ws_styles_list.append(
            slack_err_msg(ws_err_count)
        )

    return dedent('''    

Invalid Styles: {invalid}

Valid Styles:   {valid}

'''.format(invalid=left_align_list(invalid_ws_styles_list) if invalid_ws_styles_list else None,
           valid=left_align_list(valid_ws_styles_list) if valid_ws_styles_list else None))
