import math
import re
from pathlib import Path

from Cache import Cache
from CacheSet import CacheSet
from Logger import Logger
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
    logger: Logger = Logger()
    # Load config
    config_file = Path("config.txt")
    if not config_file.exists():
        logger.log_and_print("ERROR: config.txt does not exist. Exiting.")
        exit(-1)
    config_dict = read_config_file(config_file = config_file)

    # Check that trace file exists
    trace_file = Path("my_tracefile.txt")
    if not trace_file.exists():
        logger.log_and_print(f"ERROR: {trace_file.name} does not exist. Exiting.")
        exit(-1)
    logger.log(f"Using trace file: {trace_file.name}\n")

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

    logger.log("----- CALCULATED CACHE CHARACTERISTICS -----")
    logger.log(f"Number of blocks: {num_blocks} (2^{int(math.log2(num_blocks))})")
    logger.log(f"Number of sets: {num_sets}")
    index_bits = int(math.log2(num_sets))
    offset_bits = int(math.log2(block_size_bytes))
    tag_bits = 32 - index_bits - offset_bits
    logger.log(f"# of bits (tag / index / offset): {tag_bits} / {index_bits} / {offset_bits}")
    address_bits = [tag_bits, index_bits, offset_bits]

    data_bits = block_size_bytes * 8
    bits_per_block = data_bits + tag_bits + 1
    logger.log(f"Data / total bits per block: {data_bits} / {bits_per_block} bits")
    logger.log(f"Total cache size: {(bits_per_block * num_blocks) / 1024 / 8} KBytes")
    logger.log("--------------------------------------------")
    logger.log("")

    # Create sets
    cache = Cache(num_sets = num_sets, blocks_per_set = associativity, replacement_policy = replacement_policy,
                  address_bits = address_bits)

    test_metric = TestMetric(address_bits = address_bits)

    # Run the trace file
    with open(file = trace_file, mode = "r", encoding = "utf-8") as opened_trace:
        lines = opened_trace.readlines()
        line_num = 0
        for line in lines:
            if "#" in line or line == "\n":
                continue

            line_num += 1
            if line_num % 50000 == 0:
                loaded_blocks = 0
                set: CacheSet
                for set in cache.sets:
                    loaded_blocks += len(set.blocks)
                print(f"Finished: {int((line_num / len(lines)) * 100)}%. Loaded blocks: {loaded_blocks} / {num_blocks}")

            line = line.replace("\n", "")
            line = int(line)
            # print()
            cache.load_block(address = line, line_num = line_num)
            test_metric.store_access(address = line)

    logger.log("------------- SIMULATION STATS -------------")
    logger.log(f"Cache_Size: {cache_size} KBytes")
    logger.log(f"Block_Size: {block_size} words ({block_size_bytes} bytes)")
    logger.log(f"Associativity: {associativity} way")

    # Print out the correct replacement policy
    replacement_policy_string: str
    if replacement_policy == 1:
        replacement_policy_string = "LRU (least recently used)"
    elif replacement_policy == 2:
        replacement_policy_string = "Random"
    else:
        replacement_policy_string = "NMRU + Random (pseudo-LRU)"

    logger.log(f"Replacement_Policy: {replacement_policy_string}")

    cache.print_status(logger = logger)
    logger.log("--------------------------------------------")

    logger.log("")
    max_blocks_in_set = 0
    set: CacheSet
    for set in cache.sets:
        if len(set.blocks) > max_blocks_in_set:
            max_blocks_in_set = len(set.blocks)
    logger.log(f"Max number of blocks in one set: {max_blocks_in_set}")

    max_accesses_for_tag = 0
    min_accesses_for_tag = 15000000000
    for tag_index_combined in test_metric.index_tag_accesses_dict:
        num_accesses = test_metric.index_tag_accesses_dict[tag_index_combined]
        max_accesses_for_tag = max(max_accesses_for_tag, num_accesses)
        min_accesses_for_tag = min(min_accesses_for_tag, num_accesses)

    logger.log(f"Max accesses for single index/tag: {max_accesses_for_tag}")
    logger.log(f"Min accesses for single index/tag: {min_accesses_for_tag}")
    logger.log(
        f"Total cache replacements: {cache.cache_replacements} / {cache.num_accesses} ({cache.cache_replacements / cache.num_accesses})")

    logger.log("")
    logger.log(f"Unique addresses in {trace_file.name}: {len(test_metric.unique_addresses)}")
    logger.log(f"Unique indices accessed: {len(test_metric.unique_indices)} / {num_sets}")
    logger.log(f"Unique index/tags accessed: {len(test_metric.unique_index_tags)}")

    # the_cache = []
    # num_replacements = 0
    # num_hits = 0
    # test_metric = TestMetric(address_bits = address_bits)
    # with open(file = trace_file, mode = "r", encoding = "utf-8") as opened_trace:
    #     lines = opened_trace.readlines()
    #     for i in range(0, num_sets):
    #         blocks = [-1, -1, 0]
    #         the_cache.append(blocks)
    #
    #     for line in lines:
    #         line = int(line.replace("\n", ""))
    #         split_bits: list = test_metric.get_split_address_from_int(line)
    #         set_index = split_bits[1] % num_sets
    #         the_blocks = the_cache[set_index]
    #         if split_bits[0] == the_blocks[0] or split_bits[0] == the_blocks[1]:
    #             num_hits += 1
    #         else:
    #             if the_blocks[0] == -1:
    #                 the_blocks[0] = split_bits[0]
    #                 the_blocks[2] = 1
    #             elif the_blocks[1] == -1:
    #                 the_blocks[1] = split_bits[0]
    #                 the_blocks[2] = 0
    #             else:
    #                 num_replacements += 1
    #                 the_blocks[the_blocks[2]] = split_bits[0]
    #                 if the_blocks[2] == 1:
    #                     the_blocks[2] = 0
    #                 else:
    #                     the_blocks[2] = 1
    #
    # print()
    # print(f"num_hits: {num_hits}")
    # print(f"num_replacements: {num_replacements}")
