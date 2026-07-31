"""
Database access layer for the enhanced CS-340 Grazioso Salvare Dashboard.

The AnimalShelter class is responsible only for MongoDB communication.
Dashboard layout, rescue filtering, and application coordination are handled
by separate modules in the enhanced design.
"""

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from config import (
    DB_COLLECTION,
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USERNAME,
)

from database_query_service import DatabaseQueryService


class AnimalShelter:
    """Provides CRUD operations for the animal shelter MongoDB collection."""

    def __init__(self):
        """Initialize the MongoDB client, database, and collection."""
        if DB_USERNAME and DB_PASSWORD:
            connection_string = (
                f"mongodb://{DB_USERNAME}:{DB_PASSWORD}@"
                f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
            )
        else:
            connection_string = f"mongodb://{DB_HOST}:{DB_PORT}/{DB_NAME}"

        self.client = MongoClient(connection_string)
        self.database = self.client[DB_NAME]
        self.collection = self.database[DB_COLLECTION]
        self.query_service = DatabaseQueryService()

    def read_animals(self, filters=None, projection_fields=None, limit=None):
        """
        Retrieve animal records using validated filters, projection, and limit.

        Args:
            filters (dict): Requested filter criteria.
            projection_fields (list): Requested fields to return.
            limit (int): Maximum records to return.

        Returns:
            list: Matching animal records.
        """
        safe_query = self.query_service.build_safe_query(filters)
        projection = self.query_service.build_projection(projection_fields)
        safe_limit = self.query_service.validate_limit(limit)

        try:
            cursor = self.collection.find(safe_query, projection).limit(safe_limit)
            return list(cursor)
        except PyMongoError:
            return []

    def create(self, data):
        """
        Insert one animal record into the database.

        Args:
            data (dict): Animal record to insert.

        Returns:
            bool: True if the insert was acknowledged, otherwise False.
        """
        if data is None or not isinstance(data, dict):
            return False

        try:
            result = self.collection.insert_one(data)
            return result.acknowledged
        except PyMongoError:
            return False

    def read(self, query=None):
        """
        Retrieve animal records matching a MongoDB query.

        This method is kept for compatibility with the original artifact.
        It now uses the safer validated read path.
        """
        return self.read_animals(filters=query)

    def update(self, query, new_values):
        """
        Update animal records matching a validated query.

        Args:
            query (dict): MongoDB query criteria.
            new_values (dict): Fields and values to update.

        Returns:
            int: Number of modified documents.
        """
        safe_query = self.query_service.build_safe_query(query)
        safe_updates = self.query_service.build_safe_update(new_values)

        if not safe_query or not safe_updates:
            return 0

        try:
            result = self.collection.update_many(safe_query, {"$set": safe_updates})
            return result.modified_count
        except PyMongoError:
            return 0

    def delete(self, query):
        """
        Delete animal records matching a validated query.

        Args:
            query (dict): MongoDB query criteria.

        Returns:
            int: Number of deleted documents.
        """
        safe_query = self.query_service.build_safe_query(query)

        if not safe_query:
            return 0

        try:
            result = self.collection.delete_many(safe_query)
            return result.deleted_count
        except PyMongoError:
            return 0