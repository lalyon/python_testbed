import pytest
from src.python_testbed.binary_ops import BinaryFile
from src.tests.fixtures.test_binaries import testBin0, testBin1
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(funcName)s %(message)s",
                    filename="log.txt",
                    filemode="w")

@pytest.mark.parametrize("binary", [
    (testBin0),
    (testBin1)
])
def test_input(binary):
    """Testing loading file bytes"""
    contents = binary.readFileAsBytes()
    assert binary.bytes == contents
    assert contents is not None
    logging.debug(contents)
    assert contents[0][:2] == "0b"


@pytest.mark.parametrize("binary", [
    (testBin0),
    (testBin1)
])
def test_output(binary):
    """Testing writing binary info to file"""
    binary.writeToFile()
    with open(binary.filename+".zmgt", "r") as file:
        outfile_contents = file.read()
    assert outfile_contents == ("totalBytes:" + str(binary.num_bytes) +
        "\nzeroLoc:" + str(binary.zero_locs))
