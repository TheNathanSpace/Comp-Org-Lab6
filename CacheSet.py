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
        elif self.replacement_policy == 3:
            self.most_recently_used: CacheBlock = None

    def is_block_loaded(self, tag: int):
        checked_block = CacheBlock(tag)
        block: CacheBlock
        for block in self.blocks:
            if block == checked_block:
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
            # Discard block at front of list (LRU)
            discarded_block = self.most_recent_used_in_order.pop(0)
        # Random
        elif self.replacement_policy == 2:
            random_i: int = random.randrange(0, len(self.blocks))
            discarded_block: CacheBlock = self.blocks[random_i]
        # NMRU + Random (psuedo-LRU)
        else:
            # print(f"Most recently used: {self.most_recently_used.tag}")
            # Randomly select block in loaded blocks
            random_i: int = random.randrange(0, len(self.blocks))
            discarded_block: CacheBlock = self.blocks[random_i]
            # Randomly select new block if it is the most recently used
            while discarded_block == self.most_recently_used:
                # print("Selecting new one")
                random_i: int = random.randrange(0, len(self.blocks))
                discarded_block: CacheBlock = self.blocks[random_i]

        # print(f"Discarding block tag {discarded_block.tag}")
        self.blocks.remove(discarded_block)

    def access_address(self, tag: int):
        accessed: CacheBlock = CacheBlock(tag)
        # Update LRU
        if self.replacement_policy == 1:
            # Clear entire list of this tag
            while accessed in self.most_recent_used_in_order:
                self.most_recent_used_in_order.remove(accessed)
            # Add tag to the end of list
            self.most_recent_used_in_order.append(accessed)
        # Update MRU
        elif self.replacement_policy == 3:
            self.most_recently_used = accessed
