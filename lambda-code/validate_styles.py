import json
from textwrap import dedent
from tableau_xml_parser import get_tableau_styles
from helpers import pp, Alerts, err_msg


def validate_styles(style_guide_json, workbook_file):
    #
    # Parse styles from Tableau Workbook file
    #
    styles = get_tableau_styles(workbook_file)

    # # Workbook styles
    # wb_styles = styles.get('workbook_styles')
    # test_workbook(wb_styles, style_guide_json)

    # Dashboard styles
    db_styles = styles.get('dashboard_styles')
    test_dashboards(db_styles, style_guide_json)
    #
    # # Worksheet styles
    # ws_styles = styles.get('worksheet_styles')
    # test_worksheets(ws_styles, style_guide_json)

    return


def test_workbook(workbook_styles, sg):
    # print('Workbook Styles at time of testing:\n', pp(workbook_styles))
    print(dedent('''
    
        Validating all top-level WORKBOOK styles...
        '''))

    wb_err_count = 0
    for component in workbook_styles:
        styles = workbook_styles.get(component)
        for style in styles:
            s = styles.get(style)
            if s is not None:
                if 'font-size' in style:
                    if s not in sg.get('font-sizes'):
                        print(f'{Alerts.FONT_SIZE} {str(s + "pt"):20s} found in {str(component + ".")}')
                        wb_err_count += 1

                if 'font-family' in style:
                    if s not in sg.get('fonts'):
                        print(f'{Alerts.FONT_TYPE} {s:20s} found in {str(component + ".")}')
                        wb_err_count += 1

                if 'color' in style:
                    if s not in sg.get('font-colors'):
                        print(f'{Alerts.FONT_COLOR} {s:20s} found in {str(component + ".")}')
                        wb_err_count += 1

    err_msg(wb_err_count)


def test_dashboards(dashboard_styles, sg):
    # print('Dashboard Styles at time of testing:\n', pp(dashboard_styles))
    print(dedent('''

    Validating each DASHBOARD in workbook...
    '''))

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
                                print(f'{Alerts.FONT_SIZE} {str(s + "pt"):20s} found in {item:20s} of dashboard {db_name}.')
                                db_err_count += 1

                        if 'font-family' in style:
                            if s not in sg.get('fonts'):
                                print(f'{Alerts.FONT_TYPE} {s:20s} found in {item:20s} of dashboard {db_name}.')
                                db_err_count += 1

                        if 'color' in style:
                            if s not in sg.get('font-colors'):
                                print(f'{Alerts.FONT_COLOR} {s:20s} found in {item:20s} of dashboard {db_name}.')
                                db_err_count += 1

    err_msg(db_err_count)


def test_worksheets(worksheet_styles, sg):
    # print('Worksheet Styles at time of testing:\n', pp(worksheet_styles))
    print(dedent('''

    Validating each WORKSHEET in workbook...
    '''))

    ws_err_count = 0
    for worksheet_style in worksheet_styles:
        worksheet = worksheet_styles.get(worksheet_style)
        ws_name = worksheet_style
        for item in worksheet:
            styles = worksheet.get(item)
            if isinstance(styles, list):
                for style_dict in styles:
                    if isinstance(style_dict, dict):
                        for style in style_dict:
                            s = style_dict.get(style)
                            if s is not None:
                                if 'fontsize' in style:
                                    if s not in sg.get('font-sizes'):
                                        print(f'{Alerts.FONT_SIZE} {str(s + "pt"):20s} found in {item:20s} of worksheet {ws_name}.')
                                        ws_err_count += 1

                                if 'fontname' in style:
                                    if s not in sg.get('fonts'):
                                        print(f'{Alerts.FONT_TYPE} {s:20s} found in {item:20s} of worksheet {ws_name}.')
                                        ws_err_count += 1

                                if 'fontcolor' in style:
                                    if s not in sg.get('font-colors'):
                                        print(f'{Alerts.FONT_COLOR} {s:20s} found in {item:20s} of worksheet {ws_name}.')
                                        ws_err_count += 1

    err_msg(ws_err_count)


if __name__ == "__main__":
    validate_styles()
