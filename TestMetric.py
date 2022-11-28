class TestMetric:
    def __init__(self, address_bits: list):
        self.address_dict = {}
        self.address_bits: list = address_bits
        self.tag_end_bit: int = self.address_bits[0]
        self.index_end_bit: int = self.tag_end_bit + self.address_bits[1]
        self.offset_end_bit: int = self.index_end_bit + self.address_bits[2]

    def dec_to_bin(self, input: int, size: int) -> list:
        """
        Converts an int value to its binary representation (works for positive and negative numbers)
        :param input: The number to convert to binary
        :param size: The size of the number in bits
        :return: A list of single-character strings representing the number in binary (as a list, since in Python strings are immutable)
        """
        i: int = size - 1

        result = "0" * size
        result = list(result)

        onBit: str = '1'
        offBit: str = '0'
        if input < 0:
            input *= -1
            input -= 1
            onBit = '0'
            offBit = '1'

        while i != -1:
            quotient: int = int(input / 2)
            remainder: int = input % 2
            input = quotient
            if remainder == 1:
                result[i] = onBit
            else:
                result[i] = offBit
            i -= 1

        return result

    def bin_to_dec(self, input: list) -> int:
        """
        Converts a binary number to decimal
        :param input: A binary number as a list of single-character strings
        :return: The converted decimal number as an int
        """
        i: int = len(input) - 1
        mul = 1
        dec = 0
        while True:
            dec += mul * int(input[i])
            mul *= 2
            i -= 1
            if i < 0:
                break
        return dec

    def get_split_address(self, bin_address: list):
        split_address = {}
        split_address["tag"] = self.bin_to_dec(bin_address[slice(0, self.tag_end_bit)])
        split_address["index"] = self.bin_to_dec(bin_address[slice(self.tag_end_bit, self.index_end_bit)])
        split_address["offset"] = self.bin_to_dec(bin_address[slice(self.index_end_bit, self.offset_end_bit)])
        return split_address

    def store_access(self, address: int):
        bin_address = self.dec_to_bin(address, 32)
        split_addresses = self.get_split_address(bin_address)

        tag: int = split_addresses["tag"]
        index: int = split_addresses["index"]
        offset: int = split_addresses["offset"]

        if index not in self.address_dict:
            self.address_dict[index] = {}
        if tag not in self.address_dict[index]:
            self.address_dict[index][tag] = 0

        self.address_dict[index][tag] = self.address_dict[index][tag] + 1

    def get_split_address_from_int(self, dec_address: int):
        bin_address = self.dec_to_bin(dec_address, 32)
        split_addresses = self.get_split_address(bin_address)

        tag: int = split_addresses["tag"]
        index: int = split_addresses["index"]
        offset: int = split_addresses["offset"]

        return [tag, index, offset]
