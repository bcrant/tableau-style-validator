import json
from tableau_xml_parser import get_tableau_styles
from helpers import pp, Alerts


def validate_styles():
    #
    # Load Style Guide
    #
    sg_json = json.load(open('./tests/sg_example.json', 'r'))
    sg_json.pop('_README')

    #
    # Load Styles from Workbook
    #
    styles = get_tableau_styles()

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
    print()
    print('Validating all top-level workbook styles...\n')

    for component in workbook_styles:
        styles = workbook_styles.get(component)
        for style in styles:
            s = styles.get(style)
            if 'font-size' in style:
                if s not in sg.get('font-sizes'):
                    print(f'{Alerts.FONT_SIZE} "{s}pt" found in {component.upper()}.')

            if 'font-family' in style:
                if s not in sg.get('fonts'):
                    print(f'{Alerts.FONT_TYPE} "{s}" found in {component.upper()}.')

            if 'color' in style:
                if s not in sg.get('font-colors'):
                    print(f'{Alerts.FONT_COLOR} "{s}" found in {component.upper()}.')


def test_dashboards(dashboard_styles, sg):
    print()
    print('Validating each dashboard in workbook...\n')

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
                            print(f'{Alerts.FONT_SIZE} "{s}pt" found in {item.upper()} of dashboard "{db_name}".')

                    if 'font-family' in style:
                        if s not in sg.get('fonts'):
                            print(f'{Alerts.FONT_TYPE} "{s}" found in {item.upper()} of dashboard "{db_name}".')

                    if 'color' in style:
                        if s not in sg.get('font-colors'):
                            print(f'{Alerts.FONT_COLOR} "{s}" found in {item.upper()} of dashboard "{db_name}".')


def test_worksheets(worksheet_styles, sg):
    print()
    print('Validating each worksheet in workbook...\n')

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
                                        f'{Alerts.FONT_SIZE} "{s}pt" found in {item.upper()} of worksheet "{ws_name}".')

                            if 'fontname' in style:
                                if s not in sg.get('fonts'):
                                    print(
                                        f'{Alerts.FONT_TYPE} "{s}" found in {item.upper()} of worksheet "{ws_name}".')

                            if 'fontcolor' in style:
                                if s not in sg.get('font-colors'):
                                    print(
                                        f'{Alerts.FONT_COLOR} "{s}" found in {item.upper()} of worksheet "{ws_name}".')


if __name__ == "__main__":
    validate_styles()
