import pymongo


class MongoDB(object):

    def __init__(self, url, db):
        self._mongo_client = pymongo.MongoClient(url)
        self._mongodb = self._mongo_client[db]

    def get_db_instance(self):
        if self._mongodb is not None:
            return self._mongodb

    def __del__(self):
        self._mongo_client.close()
