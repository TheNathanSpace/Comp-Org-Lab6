class CacheBlock:
    def __init__(self, tag: int):
        self.tag = tag

    def tags_are_equal(self, tag: int):
        return self.tag == tag

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, CacheBlock):
            return self.tag == other.tag
        return False
