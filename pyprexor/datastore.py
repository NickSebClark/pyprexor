class Datastore:
    def get_parameter_set(self, id: int):
        raise NotImplementedError

    def write_process_data(self, data: dict):
        raise NotImplementedError


class InMemoryDataStore(Datastore):
    def __init__(self, parameter_sets: list[dict], key: str = "id"):
        self.parameter_sets = parameter_sets
        self.process_data = []
        self.key = key

    def get_parameter_set(self, id: int):
        return [parameter_set for parameter_set in self.parameter_sets if parameter_set[self.key] == id][0]

    def write_process_data(self, process_data: dict):
        self.process_data.append(process_data)

    def read_all_process_data(self):
        return self.process_data
