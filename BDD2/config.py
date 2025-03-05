import sqlite3
from sqlalchemy.engine import Engine
from sqlalchemy import event

class Config:
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection): 
        dbapi_connection.execute("PRAGMA foreign_keys=ON;")