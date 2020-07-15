import pytest
from src.python_testbed.binary_ops import BinaryFile
from src.tests.fixtures.test_binaries import testBin0, testBin1
from src.tests.fixtures.answers.zeroLocsAnswer import testBinZeroAns0, testBinZeroAns1
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(funcName)s %(message)s",
                    filename="log.txt",
                    filemode="w")


@pytest.mark.parametrize("binary, expected_len", [
    (testBin0, 51),
    (testBin1, 883)
])
def test_totalBytes(binary, expected_len):
    """Testing function that returns num of bytes in file"""
    num = binary.totalBytes()
    assert binary.num_bytes == expected_len
    assert num == expected_len

@pytest.mark.parametrize("binary, answer_dict", [
    (testBin0, testBinZeroAns0),
    (testBin1, testBinZeroAns1)
])
def test_zeroByte(binary, answer_dict):
    """Testing function that finds zero byte locations"""
    zero_locs = binary.zeroByte()
    assert binary.zero_locs == answer_dict
    assert zero_locs == answer_dict
