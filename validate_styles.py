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

    # # Dashboard styles
    # db_styles = styles.get('dashboard_styles')
    #
    # # Worksheet styles
    # ws_styles = styles.get('worksheet_styles')
    return


def test_workbook(workbook_styles, sg):
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


if __name__ == "__main__":
    validate_styles()
