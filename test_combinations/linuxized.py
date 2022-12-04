import math
from pathlib import Path

from src.Cache import Cache


def run_test(associativity: int, replacement_policy: int, cache_size: int, block_size: int):
    # Check that trace file exists
    trace_file = Path("../tracefile.txt")
    if not trace_file.exists():
        print(f"ERROR: {trace_file.name} does not exist. Exiting.")
        exit(-1)

    # Calculate sizes and stuff
    block_size_bytes = block_size * 4
    set_size_bytes = associativity * block_size_bytes
    cache_size_bytes = cache_size * 1024
    num_blocks = int(cache_size_bytes / block_size_bytes)
    num_sets = int(cache_size_bytes / set_size_bytes)

    # Calculate number of bits
    index_bits = int(math.log2(num_sets))
    offset_bits = int(math.log2(block_size_bytes))
    tag_bits = 32 - index_bits - offset_bits
    address_bits = [tag_bits, index_bits, offset_bits]

    # Size of cache
    data_bits = block_size_bytes * 8
    bits_per_block = data_bits + tag_bits + 1

    # Create sets
    cache = Cache(num_sets = num_sets, blocks_per_set = associativity, replacement_policy = replacement_policy,
                  address_bits = address_bits)

    # Run the trace file
    with open(file = trace_file, mode = "r", encoding = "utf-8") as opened_trace:
        lines = opened_trace.readlines()
        line_num = 0
        for line in lines:
            # Skip comments or blank lines
            if "#" in line or line == "\n":
                continue

            # Parse address and send it to the simulation
            line = line.replace("\n", "")
            line = int(line)
            cache.load_block(address = line)

    hit_rate = cache.num_hits / cache.num_accesses

    to_write = f"{associativity} {replacement_policy} {cache_size} {block_size} {hit_rate}\n"
    output = Path("tested_output.txt")
    output.touch(exist_ok = True)
    with open(file = output, encoding = "utf-8", mode = "a") as opened:
        opened.write(to_write)
