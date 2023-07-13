import subprocess
import pytest

def datasets():
    test_datasets = [
        {
            "program_file": "test/add.stml",
            "expected": "30\n"
        },
        {
            "program_file": "test/sub.stml",
            "expected": "10\n"
        },
        {
            "program_file": "test/fibonacci1.stml",
            "expected": "55\n"
        },
        {
            "program_file": "test/fibonacci2.stml",
            "expected": "1\n1\n2\n3\n5\n8\n13\n21\n34\n55\n"
        },
    ]

    for d in test_datasets:
        yield pytest.param(d["program_file"], d["expected"], id=d["program_file"])

@pytest.mark.parametrize("program_file, expected", datasets())
def test_stack_machine(program_file, expected):
    result = subprocess.run(["python3", "stm.py", program_file], capture_output=True)
    assert result.stdout.decode("utf-8") == expected

