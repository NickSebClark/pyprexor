import inspect
import pyprexor.datastore as ds
import pyprexor
from datetime import datetime
import getpass
import importlib.metadata

datastore: ds.Datastore
sw_version = "0.0.0"


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
        process_data["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        process_data["user"] = getpass.getuser()
        process_data["sw_version"] = sw_version
        process_data["data"] = result
        process_data["name"] = self.func.__name__

        datastore.write_process_data(process_data)

        # write the result to the db
        return result


def initialise(store: ds.Datastore):
    global datastore
    datastore = store

    current_frame = inspect.currentframe()

    # Get the caller's frame
    caller_frame = current_frame.f_back

    # Get the caller's module
    caller_module = inspect.getmodule(caller_frame)

    # Get the caller's package
    caller_package = caller_module.__package__

    global sw_version

    sw_version = caller_package

    import __main__

    print(__main__.__file__)
