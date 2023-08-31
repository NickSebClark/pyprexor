from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pyprexor_datastore.datastore import Datastore


class MongoDataStore(Datastore):
    def __init__(self, uri: str, database: str = "pyprexor"):
        client: MongoClient = MongoClient(uri, server_api=ServerApi("1"))

        try:
            client.admin.command("ping")
            print("Successfully connected to MongoDB!")
        except Exception as e:
            print("Error during connection to Mongo DB")
            raise e

        self.db = client[database]

    def get_parameter_set(self, id: str):
        return self.db.parameter_sets.find_one({"_id": id})

    def write_process_data(self, data: dict) -> str:
        return self.db.process_data.insert_one(data).inserted_id

    def write_parameter_set(self, parameter_set: dict) -> str:
        return self.db.parameter_sets.insert_one(parameter_set).inserted_id

    def read_all_process_data(self) -> list[dict]:
        return [data for data in self.db.process_data.find()]
