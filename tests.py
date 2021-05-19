import unittest
from validate_styles import test_workbook


class StyleTests(unittest.TestCase):
    """Tests for tableau_xml_parser."""

    #
    # Load Style Guide
    #
    sg_json = json.load(open('./tests/sg_example.json', 'r'))
    sg_json.pop('_README')

    def test_fonts(self):
        self.assertEqual(test_workbook(sg_json), 2)

        # self.assertEqual()


if __name__ == "__main__":
    unittest.main(verbosity=2)
