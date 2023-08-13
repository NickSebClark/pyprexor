import inspect


class PyProcess:
    def __init__(self, func=None):
        self.func = func

    def __call__(self, parameter_id):
        print(f"Load parameter set {parameter_id}")

        sig = inspect.signature(self.func)
        func_params = sig.parameters

        # get all the parameters from the parameter dictionary
        parameters = {}

        for name, param in func_params.items():
            print(f"Name: {name}, Kind: {param.kind}, Default: {param.default}")

            parameters[name] = param.default

        result = self.func(**parameters)

        # write the result to the db
        return result


def initialise(datastore=None, data={}, key: str = "id"):
    pass
