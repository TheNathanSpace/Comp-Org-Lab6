from src import bit_util


class SimulationMetrics:
    def __init__(self, address_bits: list):
        self.index_tag_accesses_dict = {}
        self.address_bits: list = address_bits
        self.tag_end_bit: int = self.address_bits[0]
        self.index_end_bit: int = self.tag_end_bit + self.address_bits[1]
        self.offset_end_bit: int = self.index_end_bit + self.address_bits[2]

        self.unique_index_tags = set()
        self.unique_addresses = set()
        self.unique_indices = set()

    def store_access(self, address: int):
        """
        Takes in the address being accessed and updates a lot of different tracked metrics with it
        :param address: The decimal address being accessed
        """
        tag, index, offset = bit_util.split_dec_address(dec_address = address,
                                                        tag_end_bit = self.tag_end_bit,
                                                        index_end_bit = self.index_end_bit,
                                                        offset_end_bit = self.offset_end_bit)

        tag_index_combined = bit_util.dec_to_bin(tag, self.tag_end_bit) + bit_util.dec_to_bin(index,
                                                                                              self.index_end_bit - self.tag_end_bit)
        tag_index_combined = bit_util.bin_to_dec(tag_index_combined)

        if tag_index_combined not in self.index_tag_accesses_dict:
            self.index_tag_accesses_dict[tag_index_combined] = 0
        self.index_tag_accesses_dict[tag_index_combined] = self.index_tag_accesses_dict[tag_index_combined] + 1

        self.unique_addresses.add(address)
        self.unique_index_tags.add(tag_index_combined)

        self.unique_indices.add(index)
