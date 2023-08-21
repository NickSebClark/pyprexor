import inspect
import pyprexor.datastore as ds
from datetime import datetime
import getpass

datastore: ds.Datastore
sw_version = "0.0.0"


class PyProcess:
    def __init__(self, func=None):
        self.func = func

    def __call__(self, set_id):
        print(f"Load parameter set {set_id}")

        global datastore

        # get all the parameters from the parameter dictionary
        parameter_set = datastore.get_parameter_set(set_id)

        func_signature = inspect.signature(self.func).parameters

        # loop through each item in the function signature to extract the required parameters from the parameter set.
        func_parameters = {}
        for name, param in func_signature.items():
            # is a value set in the parameter set?
            if name not in parameter_set:
                if param.default == inspect.Parameter.empty:
                    raise KeyError(f"Required parameter {name} not present in the parameter set.")
                else:
                    param_value = param.default
            else:
                param_value = parameter_set[name]
            func_parameters[name] = param_value

        result = self.func(**func_parameters)

        process_data = {}
        process_data["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        process_data["user"] = getpass.getuser()
        process_data["sw_version"] = sw_version
        process_data["data"] = result
        process_data["name"] = self.func.__name__

        # write the result to the db
        datastore.write_process_data(process_data)

        # return the result as normal in case we want to use it.
        return result


def initialise(store: ds.Datastore, version: str = ""):
    global datastore
    datastore = store

    global sw_version
    sw_version = version
