import pyprexor.core as core
from pyprexor.datastore import InMemoryDataStore
from unittest.mock import patch
from datetime import datetime
import pytest
import time
import warnings


def addition_process(a: int, b: int = 2) -> int:
    return a + b


def test_all_parameters_present():
    """Execute a process with all the parameters present and check we have the required outputs are present."""
    data_store = InMemoryDataStore([{"id": 1, "a": 1, "b": 3}])
    version = "1.0.0"
    user = "testuser"

    core.initialise(data_store, version)

    process = core.PyProcess(addition_process)

    with patch("pyprexor.core.datetime") as mock_datetime, patch("pyprexor.core.getpass") as mock_getpass:
        mock_datetime.now.return_value = datetime(2023, 8, 21, 22, 6, 42)
        mock_getpass.getuser.return_value = user
        process(1)

    process_data = data_store.read_all_process_data()[0]

    assert process_data["datetime"] == "2023-08-21 22:06:42"
    assert process_data["user"] == user
    assert process_data["data"] == 4
    assert process_data["name"] == "addition_process"
    assert process_data["sw_version"] == version


def test_default_value_used():
    """Execute a process with a missing optional parameter and check the default is used"""
    data_store = InMemoryDataStore([{"id": 1, "a": 1}])

    core.initialise(data_store)

    process = core.PyProcess(addition_process)

    process(1)

    process_data = data_store.read_all_process_data()[0]

    assert process_data["data"] == 3


def test_required_parameter_not_present():
    """Execute a process with a required parameter missing and check we get a key error"""
    data_store = InMemoryDataStore([{"id": 1, "b": 1}])

    core.initialise(data_store)

    process = core.PyProcess(addition_process)

    with pytest.raises(KeyError):
        process(1)


def test_process_timing():
    """Execute a process with slow execution and check it is timed correctly. Also tests process with no inputs."""

    def slow_process():
        time.sleep(0.01)

    data_store = InMemoryDataStore([{"id": 1}])
    core.initialise(data_store)

    process = core.PyProcess(slow_process)

    process(1)

    process_data = data_store.read_all_process_data()[0]

    assert process_data["execution_time"] >= 0.01


def test_typing_check():
    def typed_process(a: int):
        pass

    def untyped_process(a):
        pass

    data_store = InMemoryDataStore([{"id": 1, "a": 1}, {"id": 2, "a": "string"}])
    core.initialise(data_store)

    process = core.PyProcess(typed_process)

    # test corret typing. I.e. no warning raised
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        process(1)
        assert not any(issubclass(item.category, core.TypeWarning) for item in w)

    # test incorrect typing
    with pytest.warns(core.TypeWarning):
        process(2)

    # test no type hint supplied
    process_2 = core.PyProcess(untyped_process)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        process_2(1)
        assert not any(issubclass(item.category, core.TypeWarning) for item in w)
