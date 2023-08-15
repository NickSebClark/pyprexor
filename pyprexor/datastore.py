class Datastore:
    def get_parameter_set(self, id: int):
        raise NotImplementedError

    def write_process_data(self, data: dict):
        raise NotImplementedError


class InMemoryDataStore(Datastore):
    def __init__(self, parameter_sets: list[dict], key: str = "id", re_index: bool = False):
        if re_index:
            self.parameter_sets = {index: parameter_set for (index, parameter_set) in enumerate(parameter_sets)}
            for id in self.parameter_sets:
                self.parameter_sets[id]["id"] = id
        else:
            self.parameter_sets = {parameter_set[key]: parameter_set for parameter_set in parameter_sets}

        self.process_data: list[dict] = []
        self.key = key

    def get_parameter_set(self, id: int):
        return self.parameter_sets[id]

    def write_process_data(self, process_data: dict):
        self.process_data.append(process_data)

    def read_all_process_data(self):
        return self.process_data
