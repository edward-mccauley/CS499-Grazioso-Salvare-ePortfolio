"""
Configuration settings for the enhanced CS-340 Grazioso Salvare Dashboard.

This module separates database configuration from the database access class.
Sensitive values such as usernames and passwords should be supplied through
environment variables instead of being hard-coded in source code.
"""

import os


DB_HOST = os.getenv("AAC_DB_HOST", "localhost")
DB_PORT = int(os.getenv("AAC_DB_PORT", "27017"))
DB_NAME = os.getenv("AAC_DB_NAME", "aac")
DB_COLLECTION = os.getenv("AAC_DB_COLLECTION", "animals")

DB_USERNAME = os.getenv("AAC_DB_USERNAME", "")
DB_PASSWORD = os.getenv("AAC_DB_PASSWORD", "")