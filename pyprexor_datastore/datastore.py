class Datastore:
    def get_parameter_set(self, id: str) -> dict:
        raise NotImplementedError

    def write_process_data(self, data: dict) -> str:
        raise NotImplementedError


class InMemoryDataStore(Datastore):
    """Datastore which stores parameter sets and process data in memory. Parameter sets are stored as a dict of dicts.
    The top-level dict key is the id of the parameter set to allow easy access.
    The process data is simply a list of dicts.
    """

    def __init__(self, parameter_sets: list[dict], key: str = "id", re_index: bool = False):
        """Initialises datastore with a list of parametersets.

        Args:
            parameter_sets (list[dict]): Parameter sets to initialise the data store with
            key (str, optional): key string. Defaults to "id".
            re_index (bool, optional): Reinitialises the key in the param sets to numbers from 0. Defaults to False.
        """
        if re_index:
            self.parameter_sets = {str(index): parameter_set for (index, parameter_set) in enumerate(parameter_sets)}
            for id in self.parameter_sets:
                self.parameter_sets[id]["id"] = id
        else:
            self.parameter_sets = {parameter_set[key]: parameter_set for parameter_set in parameter_sets}

        self.process_data: list[dict] = []
        self.key = key

    def get_parameter_set(self, id: str) -> dict:
        """Get the parameter set from the dictionary of parameter sets

        Args:
            id (str): Id of parameter set to return.

        Returns:
            dict: Returned parameter set.
        """
        return self.parameter_sets[id]

    def write_process_data(self, process_data: dict):
        """Adds a process data dict to the store.

        Args:
            process_data (dict): Process data to add.
        """
        self.process_data.append(process_data)

    def read_all_process_data(self) -> list[dict]:
        """Gets all stored process data dicts.

        Returns:
            list[dict]: The process data in the datastore.
        """
        return self.process_data
