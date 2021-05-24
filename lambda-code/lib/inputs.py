import json
import argparse


def get_cli_input():
    """
    Accept input JSON and TWB files from the command line.

    Usage:
    $ python tableau_xml_parser.py --style-guide './tests/sg_example.json' --tableau-workbook './tests/wb_example.twb'

    """

    parser = argparse.ArgumentParser()

    # Style Guide
    parser.add_argument('-s', '--style-guide',
                        required=True,
                        help='''
                        JSON Style Guide (.json) filepath containing style standards to test against Tableau file.
                        ''',
                        type=str)

    # Tableau Workbook
    parser.add_argument('-w', '--tableau-workbook',
                        required=True,
                        help="Tableau Workbook (.twb) file to test for style guide compliance.",
                        type=str)

    arguments = parser.parse_args()

    return arguments


def ingest_style_guide(args):
    """Ingest JSON style guide file (~/foo.json) from command line arguments."""

    # Test Style Guide input for valid JSON
    with open(args.style_guide) as style_guide_infile:
        try:
            style_guide_json = json.load(style_guide_infile)

        except json.JSONDecodeError:
            print('Invalid JSON format. \n'
                  'Check for double quotes and matching brackets.')

    return style_guide_json


def ingest_tableau_workbook(args):
    """Ingest Tableau Workbook file (~/foo.twb) from command line arguments."""

    # Pass Tableau Workbook to parser as open file
    with open(args.tableau_workbook) as tableau_workbook_infile:
        tableau_workbook_file = tableau_workbook_infile.read()

    return tableau_workbook_file


if __name__ == '__main__':
    get_cli_input()
