from neo4j import (GraphDatabase, basic_auth)
import os
import atexit

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

        # Get environment variables
        USER = os.getenv('DATABASE_USERNAME')
        PASSWORD = os.getenv('DATABASE_PASSWORD')
        DB_URL = os.getenv('DATABASE_URL')

        self.driver = GraphDatabase.driver(DB_URL, auth=(USER, PASSWORD))
        return self.driver

    def get_session(self):
        return self.get_driver().session()
        
    def close_driver(self):
        if (self.driver != None):
            self.driver.close()

def exit_handler():
    NeoDB().close_driver()

atexit.register(exit_handler)