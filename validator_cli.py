import sys; sys.path.append('./lambda-code/')
import json
import argparse
from validate_styles import validate_styles


def validate_styles_local_cli():
    """
    HOW TO RUN STYLE VALIDATOR AD HOC WITH LOCAL FILES (INSTEAD OF USING AWS LAMBDA DEPLOYMENT):

    Run as Command Line Interface
    $ python validator_cli.py -s ./tests/example_style_guide.json -w ./tests/example_workbook.twb

    Run in PyCharm: PyCharm Run Config Parameters
    Script Path: ~/tableau-style-validator/validator_cli.py
    Parameters: -s"./tests/example_style_guide.json" -w"./tests/example_workbook.twb"
    """
    #
    # Get input from command line arguments
    #
    input_files = get_cli_input()

    # Style Guide
    sg_json = ingest_style_guide(input_files)
    sg_json.pop('_README')

    # Tableau Workbook
    wb_file = ingest_tableau_workbook(input_files)

    # Run Tableau Style Validator from command line inputs
    validate_styles(sg_json, wb_file)


def get_cli_input():
    """
    Accept input JSON and TWB files from the command line.

    Usage:
    $ python validator_cli.py --style-guide './tests/example_style_guide.json' \
                              --tableau-workbook './tests/example_workbook.twb'

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
    validate_styles_local_cli()
