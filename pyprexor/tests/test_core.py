import pyprexor.core as core
from pyprexor.datastore import InMemoryDataStore
from unittest.mock import patch
from datetime import datetime


def addition_process(a: int, b: int = 2) -> int:
    return a + b


def test_all_parameters_present():
    data_store = InMemoryDataStore([{"id": 1, "a": 1, "b": 2}])
    version = "1.0.0"
    user = "testuser"

    core.initialise(data_store, version)

    x = core.PyProcess(addition_process)

    with patch("pyprexor.core.datetime") as mock_datetime, patch("pyprexor.core.getpass") as mock_getpass:
        mock_datetime.now.return_value = datetime(2023, 8, 21, 22, 6, 42)
        mock_getpass.getuser.return_value = user
        x(1)

    process_data = data_store.read_all_process_data()[0]

    assert process_data["datetime"] == "2023-08-21 22:06:42"
    assert process_data["user"] == user
    assert process_data["data"] == 3
    assert process_data["name"] == "addition_process"
    assert process_data["sw_version"] == version


def test_default_value_used():
    pass


def test_required_parameter_not_present():
    pass
