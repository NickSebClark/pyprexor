import re


def my_function(arg1: int, arg2: str):
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        arg1 (int): The first parameter.
        arg2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    pass


docstring = my_function.__doc__
match = re.search(r"Args:\n(.*?)(?:\n\n|$)", docstring, re.DOTALL)  # type: ignore
if match:
    args_section = match.group(1)
    args = re.findall(r"\s*(\w+) \(([^)]+)\): (.*)", args_section)
    for name, type_, description in args:
        print(f"Name: {name}, Type: {type_}, Description: {description}")
