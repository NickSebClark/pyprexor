import pyprexor as ex
from pyprexor.datastore import InMemoryDataStore


@ex.PyProcess
def simple_process(number_1, number_2: int = 2, text_param: str = "default") -> int:
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


def main():
    ds = InMemoryDataStore(
        [{"id": 1, "number_1": 2, "number_2": 3}, {"id": 2, "number_2": 1, "text_param": "non-default"}]
    )

    ex.initialise(ds, version="ex")

    simple_process(1)

    try:
        simple_process(2)
    except KeyError:
        pass


if __name__ == "__main__":
    main()
