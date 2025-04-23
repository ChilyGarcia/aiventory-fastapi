from typing import List, Dict, Any
from databases import Database
from src.database import database
from src.auth.hashing import hash_password

class BaseSeeder:
    def __init__(self, db: Database = database):
        self.db = db

    async def seed(self) -> None:
        """Method to be implemented by concrete seeders"""
        raise NotImplementedError

    async def clear(self) -> None:
        """Method to be implemented by concrete seeders"""
        raise NotImplementedError
