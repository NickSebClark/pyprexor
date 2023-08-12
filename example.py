import pyprexor as ex


@ex.PyProcess
def simple_process(number_1: int = 1, number_2: int = 2, text_param: str = "default") -> int:
    """An example process for demonstration.

    Args:
        number_1 (int, optional): The first number argument. Defaults to 1.
        number_2 (int, optional): The second number argument. Defaults to 2.
        text_param (str, optional): Some text parameter. Defaults to "default".

    Returns:
        int: Sum of the numbers
    """
    print(f"Inside the process. Number 1 + Number 2 = {number_1+number_2}. Text parameter: {text_param}")
    return number_1 + number_2


if __name__ == "__main__":
    ex.process(simple_process, 10)
