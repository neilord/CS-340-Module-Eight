#!/usr/bin/env python
# coding: utf-8

"""
animal_shelter.py
-----------------
A Python module providing CRUD operations for a MongoDB
collection named 'animals' in the 'AAC' database.

By default, it connects as user 'root' with password 'z8H0b1BpMo'
to the Apporto host and port. Adjust as needed.
"""

from bson.objectid import ObjectId
from pymongo import MongoClient


class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB"""

    def __init__(
        self,
        username="root",
        password="z8H0b1BpMo",
        host="nv-desktop-services.apporto.com",
        port=31776,
        db_name="AAC",
        col_name="animals",
    ):
        """
        Initialize a connection to the MongoDB.
        - username/password: authentication credentials
        - host/port: location of the MongoDB instance
        - db_name/col_name: which database/collection to use
        """
        # Because 'root' was likely created in the 'admin' database, we use authSource=admin:
        auth_db = "admin"

        # Build MongoDB URI
        uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource={auth_db}"

        # Initialize the MongoClient
        self.client = MongoClient(uri)

        # Store references to the database and collection
        self.database = self.client[db_name]
        self.collection = self.database[col_name]

    def create(self, data: dict) -> bool:
        """
        Create method to insert a new document into the collection.
        Returns True if the insert is successful, else False.
        """
        if not data:
            raise ValueError("Cannot create document from empty data.")

        try:
            result = self.collection.insert_one(data)
            return result.inserted_id is not None
        except Exception as ex:
            print("Error inserting document:", ex)
            return False

    def read(self, query: dict) -> list:
        """
        Read method to query documents from the collection.
        Returns a list of documents matching 'query'; otherwise an empty list.
        """
        if query is None:
            raise ValueError("Query cannot be None.")

        try:
            # .find() returns a Cursor; convert to list
            results = self.collection.find(query)
            return list(results)
        except Exception as ex:
            print("Error reading documents:", ex)
            return []

    def update(self, query: dict, new_values: dict) -> int:
        """
        Updates document(s) matching `query` with `new_values`.
        Returns the number of documents updated.
        """
        try:
            update_result = self.collection.update_many(query, {"$set": new_values})
            return update_result.modified_count
        except Exception as ex:
            print("Error updating document(s):", ex)
            return 0

    def delete(self, query: dict) -> int:
        """
        Deletes document(s) matching `query`.
        Returns the number of documents deleted.
        """
        try:
            delete_result = self.collection.delete_many(query)
            return delete_result.deleted_count
        except Exception as ex:
            print("Error deleting document(s):", ex)
            return 0
