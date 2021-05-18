import json
import argparse

parser = argparse.ArgumentParser()

#
# Accept JSON input files
#
# Style Guide
parser.add_argument('--style-guide-infile', nargs=1,
                    help="JSON file (.json) containing style standards to test against Tableau file",
                    type=argparse.FileType('r'))

# Tableau Workbook
parser.add_argument('--twb-infile', nargs=2,
                    help="Tableau Workbook (.twb) file to test for style guide compliance.",
                    type=argparse.FileType('r'))

arguments = parser.parse_args()

# Loading a JSON object returns a dict.
d = json.load(arguments.infile[0])

print(d)
