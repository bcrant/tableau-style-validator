import json
import unittest
from tableau_xml_parser import get_tableau_styles
from helpers import pp


# class StyleTests(unittest.TestCase):
#     """Tests for tableau_xml_parser."""


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
    for s in workbook_styles:
        item = workbook_styles.get(s)
        print()
        for i in item:
            x = item.get(i)
            if 'font-size' in i:
                if x not in sg.get('font-sizes'):
                    self.assert()
                    print('Wrong font size mothafucka!!')
                    print(f'BAD STYLE. Font Size {x} found in {s.upper()}.')

            if 'font-family' in i:
                if x not in sg.get('fonts'):
                    print('The fuck you think this is??? YOU CANT USE THAT FONT BRUH')
                    print(f'BAD STYLE. Font family {x} found in {s.upper()}.')

            if 'color' in i:
                if x not in sg.get('font-colors'):
                    print('Who the fuck told you to paint outside the lines??')
                    print(f'BAD STYLE. Font color {x} found in {s.upper()}.')


if __name__ == "__main__":
    validate_styles()
