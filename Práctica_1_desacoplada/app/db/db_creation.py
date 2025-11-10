import os
from .clientDB import PostgresDatabase


class DatabaseFactory:
    @classmethod
    def create(cls):
        try:
            db = PostgresDatabase()
            return db
        except Exception as e:
            raise RuntimeError(f"Error al inicializar la base de datos PostgreSQL: {e}")