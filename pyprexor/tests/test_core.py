import pyprexor.core as core


def test_process():
    @core.PyProcess
    def simple(number_1: int = 1, number_2: int = 2):
        return number_1 + number_2

    assert core.process(simple, 10) == {"result": 3}
