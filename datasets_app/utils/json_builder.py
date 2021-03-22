""" Module to build JSON file """
import json
# Import MEDIA_ROOT
from django.conf import settings
# Mime-Type
import mimetypes


class JSONFileBuilder:
    """ Class to build JSON structure """

    def __init__(self, data):
        self.data = data

    def fill_data_points(self, data_points):
        """ Method that maps DataPoint objects in the required structure
        Args:
            data_points (list): QuerySet list for DataPoint objects
        """
        print(data_points)
        self.data_points = []
        for data_point in data_points:
            data_point_info = {
                f"{data_point.data_point_id}": {
                    "data_point_standard_name":
                        data_point.data_point_standard_name,
                    "approved_abbreviations":
                        data_point.approved_abbreviations.split('|')
                        if data_point.approved_abbreviations else "",
                    "data_point_definition":
                        data_point.data_point_definition,
                    "applicable_data_universes":
                        data_point.applicable_data_universes.split('|')
                        if data_point.applicable_data_universes else "",
                    "applicable_domicile":
                        data_point.applicable_domicile.split('|')
                        if data_point.applicable_domicile else "",
                    "data_type":
                        data_point.data_type,
                    "data_point_possible_values":
                        data_point.data_point_possible_values.split('|')
                        if data_point.applicable_domicile else "",
                    "is_derived":
                        data_point.is_derived,
                    "methodology_reference":
                        data_point.methodology_reference
                }
            }
            self.data_points.append(data_point_info)
        print("found {} datapoints".format(len(self.data_points)))

    def build_structure(self):
        """ Method that map all the required data in the desire
        structure
        """
        self.structure = {
            f"{self.data['owner_name'].replace(' ', '_')}_namespaces": {
                f"{self.data['namespace'].namespace_id}": {
                    "namespace_option_name":
                        self.data['namespace'].namespace_option_name,
                    "databases": [{
                        f"{self.data['database_name']}": self.data_points
                    }]
                }
            }
        }

    def create_json_file(self, file_name):
        """ This method creates the JSON file to download it
        Args:
            file_name (str): The desired file name given by the user
        """
        json_file = open(f"{settings.MEDIA_ROOT}{file_name}.json", "w")
        json.dump(self.structure, json_file, indent=4)
        json_file.close()

    @staticmethod
    def download_file(file_name):
        """ Creates Mime-Type downlodable file
        Args:
            file_name(str): The desired file name given by the user
        """
        json_file_path = f"{settings.MEDIA_ROOT}{file_name}.json"
        # Reads file content
        json_file = open(json_file_path, 'r')
        mime_type, _ = mimetypes.guess_type(json_file_path)
        return json_file, mime_type
