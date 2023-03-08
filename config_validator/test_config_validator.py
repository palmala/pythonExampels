import unittest
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import yaml
import xmlrunner


class TestConfig(unittest.TestCase):

    def test_xml_files(self):
        for root, dirs, files in os.walk('.'):
            for current_file in files:
                if ".xml" in current_file:
                    current_xml = os.path.join(root, current_file)
                    try:
                        tree = ET.parse(current_xml)
                        root = tree.getroot()
                        print(f"{current_xml} XML is good")
                    except ParseError:
                        print(f"{current_xml} XML is not good")

    def test_yaml_files(self):
        for root, dirs, files in os.walk('.'):
            for current_file in files:
                if ".yaml" in current_file:
                    current_yaml = os.path.join(root, current_file)
                    with open(current_yaml, 'r') as stream:
                        try:
                            content = yaml.load(stream)
                            print(f"{current_yaml} YAML is good")
                        except yaml.YAMLError as exception:
                            print(f"{current_yaml} YAML is not good")


def run_all_tests_with_xml_report():
    xml_report_dir = './xml_report'
    current_directory = os.getcwd()
    asd = os.path.join(current_directory, xml_report_dir)
    print(asd)
    output_file = open(asd, "w")
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output_file))


if __name__ == "__main__":
    run_all_tests_with_xml_report()
