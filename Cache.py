import bit_util
from CacheSet import CacheSet
from Logger import Logger


class Cache:
    def __init__(self, num_sets: int, blocks_per_set: int, replacement_policy: int, address_bits: list):
        self.num_accesses = None
        self.num_hits = None
        self.num_misses = None

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
        """
        Print the cache's simulation stats
        :param logger:
        """
        logger.log_and_print(f"Total_Number_of_Accesses: {self.num_accesses}")
        logger.log_and_print(f"Cache_Hits: {self.num_hits}")
        logger.log_and_print(f"Cache_Misses: {self.num_misses}")
        logger.log_and_print(f"Cache_Hit_Rate: {self.num_hits / self.num_accesses}")
        logger.log_and_print(f"Cache_Miss_Rate: {self.num_misses / self.num_accesses}")

    def create_sets(self, num_sets: int, blocks_per_set: int, replacement_policy: int):
        """
        Initializes all the cache sets when the Cache is created
        :param num_sets: The numbers of sets in the cache
        :param blocks_per_set: The set associativity
        :param replacement_policy: Should be one of 1, 2, 3 (see config.txt)
        """
        for i in range(num_sets):
            self.sets.append(CacheSet(blocks_per_set, replacement_policy))

    def load_block(self, address):
        """
        Load an address block into the cache, performing necessary cache replacements and updating metrics
        :param address: The address as an int
        """
        tag, index, offset = bit_util.split_dec_address(dec_address = address,
                                                        tag_end_bit = self.tag_end_bit,
                                                        index_end_bit = self.index_end_bit,
                                                        offset_end_bit = self.offset_end_bit)

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
