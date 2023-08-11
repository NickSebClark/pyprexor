import inspect

class Process:
    def __init__(self, func=None, parameter_id=None):
        self.func = func
        self.parameter_id = parameter_id

    def __call__(self):
        print(f"Load parameter set {self.parameter_id}")

        sig = inspect.signature(self.func)
        func_params = sig.parameters

        parameters = {}

        for name, param in func_params.items():
            print(f"Name: {name}, Kind: {param.kind}, Default: {param.default}")

            parameters[name] = param.default


        result = self.func(**parameters)

        #write the result to the db
        return result

@Process
def simple_process(number_1:int=1, number_2:int=2, text_param:str="default")->int:
    """An example process for demonstration.

    Args:
        number_1 (int, optional): The first number argument. Defaults to 1.
        number_2 (int, optional): The second number argument. Defaults to 2.
        text_param (str, optional): Some text parameter. Defaults to "default".

    Returns:
        int: Sum of the numbers
    """
    print(f"Inside the process. Number 1 + Number 2 = {number_1+number_2}. Text parameter: {text_param}")
    return number_1+number_2

def run_process(process_name:str, parameter_set:int=0):
    print(f"Running {process_name}")
    process = globals()[process_name]
    process.parameter_id = parameter_set
    result = process()
    print(f"Result: {result}")


if __name__ == "__main__":
    run_process("simple_process", 10)