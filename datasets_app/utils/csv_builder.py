""" Module to build CSV report """
# Import MEDIA_ROOT
from django.conf import settings
# Mime-Type
import mimetypes
import time


class CSVFileBuilder:
    """ Class to build CSV file """
    SCHEMA_ANOMALIE = "Row doesn't match with the headers schema"
    DUPLICATE_ANOMALIE = "Duplicated row in file"
    ANOMALIES = {
        "duplicated": DUPLICATE_ANOMALIE,
        "invalid_schema": SCHEMA_ANOMALIE
    }
    FILE_IDENTEFIER = {
        "namespaces_anomalies": "namespaces file",
        "columns_anomalies": "columns file",
        "datapoints_anomalies": "datapoints file"
    }

    time_file = time.strftime("%Y-%m-%dT%H%M%S")

    @classmethod
    def write_file(cls, data):
        """ Write CSV content based on data """
        csv_file = f"{settings.MEDIA_ROOT}{cls.time_file}.csv"
        with open(csv_file, 'w') as file:
            headers = "file,line,anomalie\n"
            # Write headers
            file.write(headers)
            for file_key, anomalies in data.items():
                source_file = cls.FILE_IDENTEFIER.get(file_key)
                for anomalie_key, anomalie_rows in anomalies.items():
                    anomalie_description = cls.ANOMALIES.get(anomalie_key)
                    for row in anomalie_rows:
                        file.write(
                            f"{source_file},{row},{anomalie_description}\n")

    @classmethod
    def download_file(cls):
        """ Creates Mime-Type downloadable file """
        csv_path = f"{settings.MEDIA_ROOT}{cls.time_file}.csv"
        # Reads file content
        csv_file = open(csv_path, 'r')
        mime_type, _ = mimetypes.guess_type(csv_path)
        return csv_file, mime_type
