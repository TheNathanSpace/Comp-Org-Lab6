import json
import math
import re
from pathlib import Path

from Cache import Cache
from CacheSet import CacheSet
from TestMetric import TestMetric


def read_config_file(config_file: Path):
    """
    Reads the config.txt file and returns a dict of the values
    :param config_file: The Path object of the config.txt file
    :return: A dict of the config values
    """
    config_dict = {}
    with open(file = config_file, mode = "r", encoding = "utf-8") as opened:
        lines = opened.readlines()
        for line in lines:
            # Comment line
            if re.match(string = line, pattern = " *#.*"):
                continue
            # Blank line
            elif re.match(string = line, pattern = "^ *$"):
                continue
            # Config line
            elif re.match(string = line, pattern = "^ *([^ ]*) *= *(\d*) *$"):
                matched = re.match(string = line, pattern = "^ *([^ ]*) *= *(\d*) *$")
                config_dict[matched.group(1)] = int(matched.group(2))
            # Assume everything else is an error
            else:
                line_stripped = line.replace("\n", "")
                print(f"ERROR: Invalid line in config.txt:\n{line_stripped}\nExiting.")
                exit(-1)
    return config_dict


if __name__ == '__main__':
    # Load config
    config_file = Path("config.txt")
    if not config_file.exists():
        print("ERROR: config.txt does not exist. Exiting.")
        exit(-1)
    config_dict = read_config_file(config_file = config_file)
    print(json.dumps(config_dict, indent = 4))

    # Check that trace file exists
    trace_file = Path("tracefile.txt")
    if not trace_file.exists():
        print("ERROR: tracefile.txt does not exist. Exiting.")
        exit(-1)

    associativity = config_dict["associativity"]
    replacement_policy = config_dict["replacement-policy"]
    cache_size = config_dict["cache-size"]
    block_size = config_dict["block-size"]

    # Get sizes in bytes (from words)
    block_size_bytes = block_size * 4
    set_size_bytes = associativity * block_size_bytes
    cache_size_bytes = cache_size * 1024
    num_blocks = int(cache_size_bytes / block_size_bytes)
    num_sets = int(cache_size_bytes / set_size_bytes)

    print()
    print(f"Number of blocks: {num_blocks} (2^{int(math.log2(num_blocks))})")
    print(f"Number of sets: {num_sets}")
    index_bits = int(math.log2(num_sets))
    offset_bits = int(math.log2(block_size_bytes))
    tag_bits = 32 - index_bits - offset_bits
    print(f"tag / index / offset: {tag_bits} / {index_bits} / {offset_bits}")
    address_bits = [tag_bits, index_bits, offset_bits]

    data_bits = block_size_bytes * 8
    print(f"Data bits per block: {data_bits}")
    bits_per_block = data_bits + tag_bits + 1
    print(f"Bits per block: {bits_per_block}")
    print(f"Total cache size: {(bits_per_block * num_blocks) / 1024 / 8} KBytes")
    print()

    # Create sets
    cache = Cache(num_sets = num_sets, blocks_per_set = associativity, replacement_policy = replacement_policy,
                  address_bits = address_bits)

    test_metric = TestMetric(address_bits = address_bits)

    unique_addresses = set()
    # Run the trace file
    with open(file = trace_file, mode = "r", encoding = "utf-8") as opened_trace:
        lines = opened_trace.readlines()
        line_num = 0
        for line in lines:
            line_num += 1
            if line_num % 50000 == 0:
                print(f"Finished: {int((line_num / len(lines)) * 100)}%")

            line = line.replace("\n", "")
            line = int(line)
            unique_addresses.add(line)
            # print()
            cache.load_block(address = line, line_num = line_num)
            test_metric.store_access(address = line)

    print()
    print(f"Cache_Size: {cache_size} KBytes")
    print(f"Block_Size: {block_size} words ({block_size_bytes} bytes)")
    print(f"Associativity: {associativity} way")

    replacement_policy_string: str
    if replacement_policy == 1:
        replacement_policy_string = "LRU (least recently used)"
    elif replacement_policy == 2:
        replacement_policy_string = "Random"
    else:
        replacement_policy_string = "NMRU + Random (pseudo-LRU)"

    print(f"Replacement_Policy: {replacement_policy_string}")

    cache.print_status()

    print()
    print(f"Number of sets: {len(cache.sets)}")
    max_blocks_in_set = 0
    set: CacheSet
    for set in cache.sets:
        if len(set.blocks) > max_blocks_in_set:
            max_blocks_in_set = len(set.blocks)
    print(f"Max number of blocks in one set: {max_blocks_in_set}")

    print(f"Accessed indices: {len(test_metric.address_dict)}")
    max_accesses_for_tag = 0
    min_accesses_for_tag = 15000000000
    for index in test_metric.address_dict:
        for tag in test_metric.address_dict[index]:
            num_accesses = test_metric.address_dict[index][tag]
            max_accesses_for_tag = max(max_accesses_for_tag, num_accesses)
            min_accesses_for_tag = min(min_accesses_for_tag, num_accesses)

    print(f"Max accesses for single tag: {max_accesses_for_tag}")
    print(f"Min accesses for single tag: {min_accesses_for_tag}")

    print(
        f"Total cache replacements: {cache.cache_replacements} / {cache.num_accesses} ({cache.cache_replacements / cache.num_accesses}%)")
    print(f"Unique addresses: {len(unique_addresses)}")
