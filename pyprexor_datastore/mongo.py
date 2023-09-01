from pyprexor_datastore.datastore import Datastore
import pymongo


class MongoDataStore(Datastore):
    """Basic wrapper around pymongo calls to MongoDB for pyprexor."""

    def __init__(self, uri: str, database: str = "pyprexor"):
        client: pymongo.MongoClient = pymongo.MongoClient(uri)

        # check we have a good connection
        with pymongo.timeout(0.5):
            client.admin.command("ping")

        self.db = client[database]

    def get_parameter_set(self, id: str) -> dict:
        """Get a parameter set from the parameter_sets collection

        Args:
            id (str): Id of parameter set to get.

        Raises:
            KeyError: pymongo find returns none when no document is found. We want a KeyError in this case.

        Returns:
            dict: Parameter set
        """
        ps = self.db.parameter_sets.find_one({"_id": id})
        if ps:
            return ps
        else:
            raise KeyError(f"Parameter set id {id} not present")

    def write_process_data(self, data: dict) -> str:
        """Write process data object to process_data collection.

        Args:
            data (dict): Data to write

        Returns:
            str: Inserted Id
        """
        return self.db.process_data.insert_one(data).inserted_id

    def write_parameter_set(self, parameter_set: dict) -> str:
        """Write parameter set to parameter_sets collection.

        Args:
            parameter_set (dict): Data to write

        Returns:
            str: Inserted id
        """
        return self.db.parameter_sets.insert_one(parameter_set).inserted_id

    def read_all_process_data(self) -> list[dict]:
        """Get all the documents present in the process_data collection.

        Returns:
            list[dict]: List of documents
        """
        return [data for data in self.db.process_data.find()]
