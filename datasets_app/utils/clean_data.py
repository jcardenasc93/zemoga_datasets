""" clean_data module to identify erros in csv files """
import csv
from django.conf import settings as project_settings
# Pandas library to handle dataframe
import pandas as pd

# Mongo connector
from datasets_app.utils.mongo_utils import MongoConnector

# Models
from datasets_app.models import Namespace, Column, DataPoint


class DataClenaer:
    """ This class clean data comming from csv files prior to
    process the data
    """

    def __init__(self, csv_file_path):
        self.csv_file_path = f"{project_settings.MEDIA_ROOT}{csv_file_path}"
        self.no_matching_schema = []
        self.df = None

    def _change_sepparator(self, row):
        """ Checks if row sepparator is ';' to use as sepparator """
        # Checks if sepparator is ';'
        return row[0].split(';')

    def find_duplicates(self):
        """ Method to find duplicated data in dataframe """
        duplicated = self.df[self.df.duplicated()]
        # Get duplicated csv indexes
        self.duplicated_rows = list(map(lambda i: i + 2, duplicated.index))
        # Removes duplicates
        self.df.drop(duplicated.index)

    def look_for_dirty(self):
        """ This method looks for anomalies in the dataframe """
        self.anomalies = None
        pass

    def fix_data_frame(self, dataset_id):
        """ This method lookups for no matching rows with schema """
        with open(self.csv_file_path, encoding='utf-8-sig') as csv_file:
            rows = csv.reader(csv_file)
            headers = next(rows)
            if len(headers) == 1:
                headers = self._change_sepparator(headers)
            schema_len = len(headers)
            row_number = 2
            cleaned_data = []

            for row in rows:
                if len(row) == 1:
                    row = self._change_sepparator(row)
                if len(row) < schema_len:
                    # Fills missing fields with NULL
                    row = row + ["" for _ in range(schema_len - len(row))]
                    self.no_matching_schema.append(row_number)
                row_number += 1
                row = row[:schema_len]
                cleaned_data.append(row)
        self.df = pd.DataFrame(cleaned_data)
        self.df.columns = headers
        self.df = self.df.assign(dataset_id=dataset_id)

    def upload_dataframe(self, collection: str):
        """ This method insert data frame records in the specified collection
        Args:
            collection (str): The database collection
        """
        # Insert mongo documents from dataframe
        data = self.df.to_dict('records')
        MongoConnector.insert_data_to_collection(collection, data)

    def get_dirty_data(self):
        """ This method retrieves csv indexes with anomalies """
        dirty_data = {
            "duplicated": self.duplicated_rows,
            "invalid_schema": self.no_matching_schema
            # Adds here more identified dirty data
            # "anomalies": self.anomalies
        }
        return dirty_data


class CleanDataset:
    """ This class holds all the clean data for a dataset """

    def __init__(self, dataset_id, namespaces_path, columns_path,
                 datapoints_path):
        self.dataset_id = dataset_id
        self.namespaces = DataClenaer(namespaces_path)
        self.columns = DataClenaer(columns_path)
        self.datapoints = DataClenaer(datapoints_path)
        self.cleaned_data = [self.namespaces, self.columns, self.datapoints]
        # Debugs data
        self._debug_data()

    def _debug_data(self):
        """ Looks for anomalies """
        # Adjust data
        for data in self.cleaned_data:
            data.fix_data_frame(self.dataset_id)
            data.find_duplicates()
            # data.look_for_dirty()

    def load_data(self):
        """ This method load dataframes to mongoDB collections """
        self.namespaces.upload_dataframe(Namespace._meta.db_table)
        self.columns.upload_dataframe(Column._meta.db_table)
        self.datapoints.upload_dataframe(DataPoint._meta.db_table)

    def retrieve_found_anomalies(self):
        """ Looks for found anomalies in the datasets """
        return {
            "namespaces_anomalies": self.namespaces.get_dirty_data(),
            "columns_anomalies": self.columns.get_dirty_data(),
            "datapoints_anomalies": self.datapoints.get_dirty_data()
        }
