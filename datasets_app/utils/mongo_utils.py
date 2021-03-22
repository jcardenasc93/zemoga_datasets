""" Includes utils methods to mongo interaction """

import os
from pymongo import MongoClient
# Project settings
from django.conf import settings as project_settings


class MongoConnector:
    """ Class that defines mongoDB connection based on pytmongo """

    @classmethod
    def _create_mongo_connection(cls):
        """ This method stabilsh mongo connection """
        params = "?retryWrites=true&w=majority"

        if os.getenv('DB_HOST'):
            host = "mongodb://{}:{}@{}:{}{}".format(
                project_settings.DB_USER, project_settings.DB_PASSWORD,
                os.getenv('DB_HOST'), os.getenv('DB_PORT'), params)
        else:
            host = "mongodb+srv://{}:{}@{}/{}{}".format(
                project_settings.DB_USER, project_settings.DB_PASSWORD,
                os.getenv('ATLAS_HOST'), project_settings.DB_NAME, params)
        return MongoClient(host)

    @classmethod
    def _connect_to_collection(cls, collection: str):
        """ Method to stabilsh access to the specified connection
        Args:
            collection (str): Collection name
        """
        # Stablish mongo connection
        mongo_db = cls._create_mongo_connection()[project_settings.DB_NAME]
        return mongo_db[collection]

    @classmethod
    def insert_data_to_collection(cls, collection: str, data: dict):
        """ Method that allows insert many data from a dataframe
        to specified collection
        Args:
            collection (str): Collection name
            data (dict): Data dictionary to insert in collection
        """
        mongo_collection = cls._connect_to_collection(collection)
        mongo_collection.insert_many(data)
