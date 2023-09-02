import pyprexor as ex


# Annotate functions we want execute with pyprexor
@ex.PyProcess
def simple_process(number_1, number_2: int = 2, text_param: str = "default") -> int:
    """An example process for demonstration.

    Args:
        number_1 (int): The first number argument.
        number_2 (int, optional): The second number argument. Defaults to 2.
        text_param (str, optional): Some text parameter. Defaults to "default".

    Returns:
        int: Sum of the numbers
    """
    print(f"Inside the process. Number 1 + Number 2 = {number_1+number_2}. Text parameter: {text_param}")
    return number_1 + number_2


def main():
    # Initialise a datastore to store parameter sets and process outputs
    datastore = ex.InMemoryDataStore(
        [{"id": 1, "number_1": 2, "number_2": 3}, {"id": 2, "number_2": 1, "text_param": "non-default"}]
    )

    # Initialise pyprexor with your datastore and version of your app.
    ex.initialise(datastore, version="0.0.0")

    # execute your process passing the parameter set id.
    simple_process(1)

    # Key erros will result if we try to execute with a parameter set missing a required parameter
    try:
        simple_process(2)
    except KeyError as key:
        print(key)

    print(datastore.read_all_process_data())


if __name__ == "__main__":
    main()
