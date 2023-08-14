import inspect
import pyprexor.datastore as ds
from typing import Type

datastore: ds.Datastore


class PyProcess:
    def __init__(self, func=None):
        self.func = func

    def __call__(self, set_id):
        print(f"Load parameter set {set_id}")

        sig = inspect.signature(self.func)
        func_params = sig.parameters

        # get all the parameters from the parameter dictionary
        parameters = datastore.get_parameter_set(set_id)

        func_parameters = {}

        for name, param in func_params.items():
            if name not in parameters:
                value = param.default
            else:
                value = parameters[name]
            func_parameters[name] = value

        result = self.func(**func_parameters)

        process_data = {}
        process_data["output"] = result
        process_data["name"] = self.func.__name__

        datastore.write_process_data(process_data)

        # write the result to the db
        return result


def initialise(store: ds.Datastore):
    global datastore
    datastore = store
