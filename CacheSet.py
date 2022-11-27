import random

from CacheBlock import CacheBlock


class CacheSet:
    def __init__(self, num_blocks: int, replacement_policy: int):
        self.num_blocks = num_blocks
        self.replacement_policy = replacement_policy
        self.blocks = list()

        # Set up LRU stuff
        if self.replacement_policy == 1:
            self.most_recent_used_in_order = list()
        elif self.replacement_policy == 2:
            self.most_recently_used = None

    def is_block_loaded(self, tag: int):
        if self.replacement_policy == 1:
            self.most_recent_used_in_order.append(CacheBlock(tag))
        elif self.replacement_policy == 3:
            self.most_recently_used = CacheBlock(tag)

        block: CacheBlock
        for block in self.blocks:
            if block.tags_are_equal(tag):
                return True
        return False

    def load_block(self, tag: int):
        # Discard block if set is full to make room for new one
        if len(self.blocks) == self.num_blocks:
            # print(f"Set is full; discarding block")
            self.discard_block()
        self.blocks.append(CacheBlock(tag))
        # print(f"Loaded block tag {tag}")

    def discard_block(self):
        discarded_block: CacheBlock
        # LRU
        if self.replacement_policy == 1:
            discarded_block = self.most_recent_used_in_order.pop()
        # Random
        elif self.replacement_policy == 2:
            random_i: int = random.randrange(0, len(self.blocks))
            discarded_block: CacheBlock = self.blocks[random_i]
        # NMRU + Random (psuedo-LRU)
        else:
            random_i: int = random.randrange(0, len(self.blocks))
            discarded_block: CacheBlock = self.blocks[random_i]
            while discarded_block == self.most_recently_used:
                random_i: int = random.randrange(0, len(self.blocks))
                discarded_block: CacheBlock = self.blocks[random_i]

        # print(f"Discarding block tag {discarded_block.tag}")
        self.blocks.remove(discarded_block)
