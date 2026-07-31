####################################################################
# CRUD_Python_Moudule.py
# Edward McCauley
# CS-340 Client Server Development
# Project 2
####################################################################

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username, password): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # Connection Variables 
        
        USER = 'REDACTED_COURSE_CREDENTIAL' 
        PASS = 'REDACTED_COURSE_CREDENTIAL' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient(f"mongodb://{USER}:{PASS}@{HOST}:{PORT}/{DB}?authSource=admin") 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
            
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        """Insert a single document into the animals collection.
        
        Args:
            data (dict): Document to instert.
            
        Returns:
            bool: True if insert succeeded, otherwise False.
        
        """
        if data is not None: 
            try:
                result = self.collection.insert_one(data)
                print("Inserted _id:", result.inserted_id)
                return result.acknowledged
            except Exception as e:
                print(f"Insert failed: {e}")
                return False
        else: 
            return False
        

    # Create method to implement the R in CRUD.
    def read(self, query):
        """Read document(s) from the animals collection using a filter.
        
        Args:
            query (dict): Filter for find().
            
        Returns:
            list: List of matching documents, or empty list on failure.        
        """
        if query is None:
            query = {}
        elif not isinstance(query, dict):
            return []
                      
        try:
            return list(self.collection.find(query))
        except Exception as e:
            print(f"Read failed: {e}")
            return []
        
        
    # Create method to implement the U in CRUD.
    def update(self, query, new_values):
        """Updates document(s) in the animals collecton.
        
        Args:
            query(dict): Filter to select documents (must not be empty).
            new_values(dict): Fields to change (key/value pairs)
        
        Returns:
            int: Number of documents modified.
        """
        if query is None or not isinstance(query, dict) or not query:
            return 0
            
        if new_values is None or not isinstance(new_values, dict) or not new_values:
            return 0
        
        try:
            result = self.collection.update_many(query, {"$set": new_values})
            return result.modified_count
        except Exception as e:
            print(f"Updated failed: {e}")
            return 0
        
        
    # Create method to implement the D in CRUD.
    def delete(self, query):
        """Delete documents(s) from the animals collection.
        
        Args:
            query (dict): Filter to select documents (must not be empty).
        
        Returns:
            int: Number of documents deleted.
        """
        # Safety: prevent accidental deletion of every document
        if query is None or not isinstance(query, dict) or not query:
            return 0
        
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print(f"Delete failed: {e}")
            return 0
        
