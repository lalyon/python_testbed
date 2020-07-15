"""Class to model the binary file, with functions to handle loading, reading, modifying files."""
from dataclasses import dataclass, field

@dataclass
class BinaryFile:
    """Class for keeping track of a binary file"""
    filename: str = ""
    bytes: tuple = ()
    num_bytes: int = 0
    zero_locs: dict = field(default_factory=dict)
    swapped_bytes: tuple = ()

    """Functions to handle file I/O"""

    def readFileAsBytes(self):
        """
        Read in a file as a bytes object

        Returns:
            bits (tuple(str)): the bytes of the file

        Example:
        >>> myBinaryFile = BinaryFile(filename="myFile.exe")
        >>> myBinaryFile.readFileAsBytes()
        (0b10101010, ...)
        """
        with open(self.filename, mode='rb') as file:
            binary_contents = file.read()
        bytes = tuple()
        for byte in binary_contents:
            # convert ints to binary representations
            bytes += (bin(byte),)
        self.bytes = bytes
        return bytes

    def writeToFile(self):
        """Write input attributes to .zmgt file"""
        with open(self.filename+".zmgt", "w") as file:
            file.write("totalBytes:" + str(self.num_bytes))
            file.write("\nzeroLoc:" + str(self.zero_locs))

    """Functions to handle byte operations"""

    def totalBytes(self):
        """Return number of bytes in the binary file"""
        # ensure we have loaded the file
        if not self.bytes:
            self.readFileAsBytes()
        self.num_bytes = len(self.bytes)
        return self.num_bytes

    def zeroByte(self):
        """
        Find locations of full zeroed bytes in input

        Returns:
            zeroLocs (dict): Locations of zero bytes, with keys representing locations,
                indexed at 1. If there are consecutive bytes of zeroes, the value of the
                key increases for each byte.

        Example:
        >>> myBinaryFile = BinaryFile(filename="myFile.jpg")
        >>> myBinaryFile.zeroByte()
        {'1': 1, '3': 2}
        """
        # ensure we know how many bytes the file contains
        if not self.num_bytes:
            self.totalBytes()
        zeroLoc = dict()
        index = 0
        # loop through bytes
        for index in range(self.num_bytes):
            consecutive_zeroes = 0
            offset = 0
            # while within bounds and a zero byte is present
            while (index + offset < self.num_bytes) and (self.bytes[index+offset] == '0b0'):
                consecutive_zeroes += 1
                offset += 1
            if consecutive_zeroes > 0:
                zeroLoc[index + 1] = consecutive_zeroes
            index += offset
        self.zero_locs = zeroLoc
        return zeroLoc

    """Functions to handle bit operations"""

    def bitSwap(self):
        """
        Swap every two bits in a file

        Returns:
            swapped_bytes: Tuple of bytes with every two bits swapped

        Note (LL):
            Using algorithm from https://www.geeksforgeeks.org/swap-every-two-bits-bytes/
        """
        # ensure we know where the zero bytes are
        if not self.zero_locs:
            self.zeroByte()
        num_bytes = self.num_bytes
        for index in range(num_bytes):
            # loop through non-zero bytes (self.zero_locs is indexed at 1)
            if index + 1 not in self.zero_locs:
                # apply mask and shift
                swapped = ((int(self.bytes[index], 2) & 0b10101010) >> 1) or ((int(self.bytes[index], 2) & 0b01010101) << 1)
                self.swapped_bytes += (bin(swapped),)
            # otherwise there is at least one zero-byte at current index
            else:
                for num_zeroes in range(self.zero_locs[index+1]):
                    self.swapped_bytes += ('0b0',)
                index += self.zero_locs[index+1]
        return self.swapped_bytes
