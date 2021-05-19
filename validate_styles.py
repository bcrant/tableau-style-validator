import json
from textwrap import dedent
from tableau_xml_parser import get_tableau_styles
from helpers import pp, Alerts
from inputs import get_cli_input, ingest_style_guide, ingest_tableau_workbook


def validate_styles():
    #
    # Get input from command line arguments
    #
    input_files = get_cli_input()

    # Style Guide
    sg_json = ingest_style_guide(input_files)
    sg_json.pop('_README')

    # Tableau Workbook
    wb_file = ingest_tableau_workbook(input_files)

    #
    # Parse styles from Tableau Workbook file
    #
    styles = get_tableau_styles(wb_file)

    # Workbook styles
    wb_styles = styles.get('workbook_styles')
    test_workbook(wb_styles, sg_json)

    # Dashboard styles
    db_styles = styles.get('dashboard_styles')
    test_dashboards(db_styles, sg_json)

    # Worksheet styles
    ws_styles = styles.get('worksheet_styles')
    test_worksheets(ws_styles, sg_json)

    return


def test_workbook(workbook_styles, sg):
    print(dedent('''
    
        Validating all top-level WORKBOOK styles...
        '''))

    for component in workbook_styles:
        styles = workbook_styles.get(component)
        for style in styles:
            s = styles.get(style)
            if 'font-size' in style:
                if s not in sg.get('font-sizes'):
                    print(f'{Alerts.FONT_SIZE} {str(s + "pt"):20s} found in {str(component + ".")}')

            if 'font-family' in style:
                if s not in sg.get('fonts'):
                    print(f'{Alerts.FONT_TYPE} {s:20s} found in {str(component + ".")}')

            if 'color' in style:
                if s not in sg.get('font-colors'):
                    print(f'{Alerts.FONT_COLOR} {s:20s} found in {str(component + ".")}')


def test_dashboards(dashboard_styles, sg):
    print(dedent('''

    Validating each DASHBOARD in workbook...
    '''))

    for dashboard in dashboard_styles:
        dashboard_style = dashboard_styles.get(dashboard)
        db_name = dashboard_style.get('db_name')
        for item in dashboard_style:
            styles = dashboard_style.get(item)
            if isinstance(styles, dict):
                for style in styles:
                    s = styles.get(style)
                    if 'font-size' in style:
                        if s not in sg.get('font-sizes'):
                            print(f'{Alerts.FONT_SIZE} {str(s + "pt"):20s} found in {item:20s} of dashboard {db_name}.')

                    if 'font-family' in style:
                        if s not in sg.get('fonts'):
                            print(f'{Alerts.FONT_TYPE} {s:20s} found in {item:20s} of dashboard {db_name}.')

                    if 'color' in style:
                        if s not in sg.get('font-colors'):
                            print(f'{Alerts.FONT_COLOR} {s:20s} found in {item:20s} of dashboard {db_name}.')


def test_worksheets(worksheet_styles, sg):
    print(dedent('''

    Validating each WORKSHEET in workbook...
    '''))

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
                            if 'fontsize' in style:
                                if s not in sg.get('font-sizes'):
                                    print(
                                        f'{Alerts.FONT_SIZE} {str(s + "pt"):20s} found in {item:20s} of worksheet {ws_name}.')

                            if 'fontname' in style:
                                if s not in sg.get('fonts'):
                                    print(
                                        f'{Alerts.FONT_TYPE} {s:20s} found in {item:20s} of worksheet {ws_name}.')

                            if 'fontcolor' in style:
                                if s not in sg.get('font-colors'):
                                    print(
                                        f'{Alerts.FONT_COLOR} {s:20s} found in {item:20s} of worksheet {ws_name}.')


if __name__ == "__main__":
    validate_styles()
