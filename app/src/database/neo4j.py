from neo4j import (GraphDatabase, basic_auth)
import os
import atexit

# Get environment variables
USER = os.getenv('DATABASE_USERNAME')
PASSWORD = os.environ.get('DATABASE_PASSWORD')
DB_URL = os.environ.get('DATABASE_URL')

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class NeoDB(Singleton):
    driver = None
    def get_driver(self):
        if (self.driver != None):
            return self.driver
        self.driver = GraphDatabase.driver(DB_URL, auth=basic_auth(USER, PASSWORD))
        return self.driver

    def get_session(self):
        if (self.driver != None):
            return self.driver.session()
        return self.get_driver().session()
        
    def close_driver(self):
        if (self.driver != None):
            self.driver.close()

def exit_handler():
    NeoDB().close_driver()

atexit.register(exit_handler)