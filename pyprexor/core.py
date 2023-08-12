import inspect


class PyProcess:
    def __init__(self, func=None, parameter_id=None):
        self.func = func
        self.parameter_id = parameter_id

    def __call__(self):
        print(f"Load parameter set {self.parameter_id}")

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


def process(process: type(callable), parameter_set: int = 0):
    data = {}

    print(f"Running {process.func.__name__}")

    process.parameter_id = parameter_set
    data["result"] = process()

    return data
