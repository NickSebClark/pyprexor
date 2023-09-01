import inspect
import pyprexor_datastore.datastore as ds
from datetime import datetime
import getpass
import time
import warnings
from typing import Any

datastore: ds.Datastore
sw_version = "0.0.0"


class TypeWarning(UserWarning):
    """Warning raised when we try a process with incorrect types"""

    pass


class PyProcess:
    """Class style decorator. Provides core Pyprexor functionality."""

    def __init__(self, func=None):
        self.func = func

    def __call__(self, set_id: str) -> Any:
        """Reads parameter set, calls the wrapped function with the parameters from the parameter set then populates a
        process data object and writes it to the datastore.

        Args:
            set_id (str): Parameter set id to pull parameters from.

        Raises:
            KeyError: Required parameter not in the parameter set.

        Returns:
            Any: Normal function return
        """
        print(f"Executing {self.func.__name__} with parameter set {set_id}...")

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
                if not param.annotation == type(parameter_set[name]) and param.annotation != inspect._empty:
                    warnings.warn(
                        f"Typing for input {name} does not match. Found: {type(parameter_set[name])} "
                        f"Expected: {param.annotation}",
                        TypeWarning,
                    )
                param_value = parameter_set[name]
            func_parameters[name] = param_value

        t0 = time.time()
        result = self.func(**func_parameters)
        t1 = time.time()

        print(f"...completed in {t1-t0:.3f} seconds.")

        process_data = {}
        process_data["name"] = self.func.__name__
        process_data["parameter_set_id"] = set_id
        process_data["sw_version"] = sw_version
        process_data["user"] = getpass.getuser()
        process_data["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        process_data["execution_time"] = t1 - t0
        process_data["data"] = result

        # write the result to the db
        datastore.write_process_data(process_data)

        # return the result as normal in case we want to use it.
        return result


def initialise(store: ds.Datastore, version: str = ""):
    """Initialises globals used by pyprexor.

    Args:
        store (ds.Datastore): Datastore object to use.
        version (str, optional): Version string to store in process data. Defaults to "".
    """
    global datastore
    datastore = store

    global sw_version
    sw_version = version
