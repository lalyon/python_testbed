import pytest
from src.python_testbed.binary_ops import BinaryFile
from src.tests.fixtures.test_binaries import testBin0, testBin1
from src.tests.fixtures.answers.bitSwapAnswer import testBinSwapAns0, testBinSwapAns1
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(funcName)s %(message)s",
                    filename="log.txt",
                    filemode="w")


@pytest.mark.parametrize("binary, answer", [
    (testBin0, testBinSwapAns0),
    (testBin1, testBinSwapAns1)
])
def test_bitSwap(binary, answer):
    """Testing function that returns num of bytes in file"""
    swapped = binary.bitSwap()
    assert swapped == answer
    assert binary.swapped_bytes == answer
