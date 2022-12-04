from pathlib import Path


class MyTestResult:
    def __init__(self, associativity: int, replacement_policy: int, cache_size: int, block_size: int, hit_rate: float):
        self.associativity: int = associativity
        self.replacement_policy: int = replacement_policy
        self.cache_size: int = cache_size
        self.block_size: int = block_size
        self.hit_rate: float = hit_rate

    def __str__(self):
        return f"{self.associativity} {self.replacement_policy} {self.cache_size} {self.block_size} {self.hit_rate}"


if __name__ == "__main__":
    input = Path("tested_output.txt")
    results = []
    with open(file = input, encoding = "utf8", mode = "r") as opened:
        for line in opened.readlines():
            split_line = line.split(" ")
            result = MyTestResult(int(split_line[0]),
                                  int(split_line[1]),
                                  int(split_line[2]),
                                  int(split_line[3]),
                                  float(split_line[4])
                                  )
            results.append(result)

    results.sort(key = lambda x: x.hit_rate, reverse = True)
    output = Path("tested_output_sorted.txt")
    output.write_text("")
    with open(file = output, encoding = "utf8", mode = "a") as opened:
        opened.write("# Associativity | Replacement policy | Cache size (kb) | Block size (words)\n")
        for result in results:
            opened.write(f"{result}\n")

    cache_sizes = dict()
    for result in results:
        if result.cache_size not in cache_sizes:
            cache_sizes[result.cache_size] = []
        cache_sizes[result.cache_size].append(result)

    for size in cache_sizes:
        cache_sizes[size].sort(key = lambda x: x.hit_rate, reverse = True)

    output = Path("tested_output_sorted_sizes.txt")
    output.write_text("")
    with open(file = output, encoding = "utf8", mode = "a") as opened:
        opened.write("# Associativity | Replacement policy | Cache size (kb) | Block size (words)\n")
        for size in cache_sizes:
            for result in cache_sizes[size]:
                opened.write(f"{result}\n")
            opened.write("\n\n# Associativity | Replacement policy | Cache size (kb) | Block size (words)\n")
