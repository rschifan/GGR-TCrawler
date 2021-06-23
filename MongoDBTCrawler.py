from TCrawler import TCrawler
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from pymongo.errors import CursorNotFound
from configparser import RawConfigParser
from pprint import pprint

class MongoDBTCrawler(TCrawler):

    def __init__(self, collection='main'):
        TCrawler.__init__(self)  
        self.collection = collection
        self.load_db_config(self.config_file)
        self.init_db()

    def load_db_config(self, config_file):
        #Read config.ini file
        config_object = RawConfigParser()
        config_object.read(config_file)

        db_conf = config_object["MONGODB"]
        self.database = db_conf['db']
        self.hostname = db_conf['hostname']
        self.port = int(db_conf['port'])
        print('loaded mongodb settings')

    def init_db(self):
        self.client = MongoClient(self.hostname, self.port)
        self.handler = self.client[self.database]
        print(self.handler)


    def save(self, json_response):
        
        if 'data' in json_response:
        
            for post in json_response['data']:
                post["_id"] = post['id']

            try:
                self.handler[self.collection].posts.insert_many(json_response['data'], ordered=False)
            except BulkWriteError as err:
                if self.verbose:
                    print(err)
            except Exception as ex:
                if self.verbose:
                    print(ex)

        if 'includes' in json_response:

            keys = ['users', 'places', 'media']
            ids_name = {
                'users':'id',
                'places':'id',
                'media':'media_key'
            }

            for k in keys:
                if k in json_response['includes']:
                    for current in  json_response['includes'][k]:
                        current["_id"] = current[ids_name[k]]
                    try:
                        self.handler[self.collection][k].insert_many(json_response['includes'][k], ordered=False)
                    except BulkWriteError as err:
                        if self.verbose:
                            print(err)
                    except Exception as ex:
                        if self.verbose:
                            print(ex)


