import pytest
from convert_rpn import convert

def datasets():
    test_datasets = [
        {
            "infix": "1 + 1",
            "rpn": "1 1 +"
        },
        {
            "infix": "1 + 1 * 2",
            "rpn": "1 1 2 * +"
        },
        {
            "infix": "( 1 + 1 ) * 2",
            "rpn": "1 1 + 2 *"
        },
        {
            "infix": "( 2 * ( 3 - 1 ) ) * 2 + 4",
            "rpn": "2 3 1 - * 2 * 4 +"
        },
    ]

    for d in test_datasets:
        yield pytest.param(d["infix"], d["rpn"], id=d["infix"])

@pytest.mark.parametrize("infix, rpn", datasets())
def test_convert_rpn(infix, rpn):
    actual = " ".join(convert(infix))
    assert actual == rpn

