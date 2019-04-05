import pytest
from query_builder.domain_model.dtos import Step, Threshold


def build_step(operator, value):
    threshold = Threshold(operator, value)
    return Step('FAKE-UUID-001', 1, "ASSET", threshold=threshold)


@pytest.mark.parametrize("resp_size,operator,value,outcome", [
    (10, "lt", 11, True),
    (10, "lt", 10, False),
    (10, "le", 10, True),
    (11, "le", 10, False),
    (10, "eq", 10, True),
    (11, "eq", 10, False),
    (11, "ne", 10, True),
    (10, "ne", 10, False),
    (10, "ge", 10, True),
    (10, "ge", 11, False),
    (11, "gt", 10, True),
    (10, "gt", 10, False)
])
def test_threshold(resp_size, operator, value, outcome):
    assert build_step(operator, value).threshold_satisfied(resp_size) == outcome
