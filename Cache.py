from CacheSet import CacheSet
from Logger import Logger


class Cache:
    def __init__(self, num_sets: int, blocks_per_set: int, replacement_policy: int, address_bits: list):
        self.num_sets: int = num_sets
        self.sets: list = list()
        self.blocks_per_set: int = blocks_per_set

        self.address_bits: list = address_bits
        self.tag_end_bit: int = self.address_bits[0]
        self.index_end_bit: int = self.tag_end_bit + self.address_bits[1]
        self.offset_end_bit: int = self.index_end_bit + self.address_bits[2]

        self.create_sets(num_sets, blocks_per_set, replacement_policy)
        self.init_metrics()

        self.cache_replacements = 0

    def init_metrics(self):
        self.num_accesses: int = 0
        self.num_hits: int = 0
        self.num_misses: int = 0

    def cache_hit(self):
        self.num_accesses += 1
        self.num_hits += 1

    def cache_miss(self):
        self.num_accesses += 1
        self.num_misses += 1

    def print_status(self, logger: Logger):
        logger.log(f"Total_Number_of_Accesses: {self.num_accesses}")
        logger.log(f"Cache_Hits: {self.num_hits}")
        logger.log(f"Cache_Misses: {self.num_misses}")
        logger.log(f"Cache_Hit_Rate: {self.num_hits / self.num_accesses}")
        logger.log(f"Cache_Miss_Rate: {self.num_misses / self.num_accesses}")

    def create_sets(self, num_sets: int, blocks_per_set: int, replacement_policy: int):
        for i in range(num_sets):
            self.sets.append(CacheSet(blocks_per_set, replacement_policy))

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

    def load_block(self, address, line_num):
        """
        Load an address block into the cache
        :param address: The address as an int
        """
        bin_address = self.dec_to_bin(address, 32)
        split_addresses = self.get_split_address(bin_address)

        tag: int = split_addresses["tag"]
        index: int = split_addresses["index"]
        offset: int = split_addresses["offset"]

        cache_set: CacheSet = self.sets[index % self.num_sets]
        cache_hit = cache_set.is_block_loaded(tag)

        if cache_hit:
            # print(f"Loading address {address} (split: {tag} / {index} / {offset}), set {index % self.num_sets}--HIT")
            self.cache_hit()
        else:
            # print(f"Loading address {address} (split: {tag} / {index} / {offset}), set {index % self.num_sets}--MISS")
            self.cache_miss()
            if len(cache_set.blocks) == cache_set.num_blocks:
                self.cache_replacements += 1
            cache_set.load_block(tag)
        cache_set.access_address(tag)
