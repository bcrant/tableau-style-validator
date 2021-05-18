import json
import pprint
import argparse


def parser_cli():
    """
    Accept input JSON and TWB files from the command line.

    Usage:
    $ python cli_input_parser.py --style-guide './company_style_rules.json' --tableau-workbook './fancy_graphs.twb'

    """

    parser = argparse.ArgumentParser()

    # Style Guide
    parser.add_argument('-s', '--style-guide',
                        required=True,
                        help='''
                        JSON Style Guide (.json) filepath containing style standards to test against Tableau file.
                        See alksdfjal;skdfja;lsdkfj
                        ''',
                        type=str)

    # Tableau Workbook
    parser.add_argument('-w', '--tableau-workbook',
                        required=False,
                        help="Tableau Workbook (.twb) file to test for style guide compliance.",
                        type=argparse.FileType('r'))

    arguments = parser.parse_args()

    # Test Style Guide input for valid JSON
    with open(arguments.style_guide) as json_style_guide:
        try:
            sg = json.load(json_style_guide)

        except json.JSONDecodeError:
            print('Invalid JSON format. \n'
                  'Check for double quotes and matching brackets.')

    pprint.pprint(sg)
    # print(type(sg))
    # datboi = json.dumps(sg, indent=4, sort_keys=True)

    return


if __name__ == '__main__':
    parser_cli()
