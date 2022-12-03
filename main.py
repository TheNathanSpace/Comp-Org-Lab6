import math
import re
from pathlib import Path

from Cache import Cache
from CacheSet import CacheSet
from Logger import Logger
from SimulationMetrics import SimulationMetrics


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
            elif re.match(string = line, pattern = "^ *([^ ]*) *= *(\d*.*\d*) *$"):
                matched = re.match(string = line, pattern = "^ *([^ ]*) *= *(\d*.*\d*) *$")
                try:
                    config_dict[matched.group(1)] = int(matched.group(2))
                except:
                    config_dict[matched.group(1)] = float(matched.group(2))

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
    trace_file = Path("tracefile.txt")
    if not trace_file.exists():
        logger.log_and_print(f"ERROR: {trace_file.name} does not exist. Exiting.")
        exit(-1)
    logger.log(f"Using trace file: {trace_file.name}\n")

    # Get config settings
    associativity = config_dict["associativity"]
    replacement_policy = config_dict["replacement-policy"]
    cache_size = config_dict["cache-size"]
    block_size = config_dict["block-size"]

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

    logger.log("----- CALCULATED CACHE CHARACTERISTICS -----")
    logger.log(f"Number of blocks: {num_blocks} (2^{int(math.log2(num_blocks))})")
    logger.log(f"Number of sets: {num_sets}")
    logger.log(f"# of bits (tag / index / offset): {tag_bits} / {index_bits} / {offset_bits}")

    # Size of cache
    data_bits = block_size_bytes * 8
    bits_per_block = data_bits + tag_bits + 1
    logger.log(f"Data / total bits per block: {data_bits} / {bits_per_block} bits")
    logger.log(f"Total cache size: {(bits_per_block * num_blocks) / 1024 / 8} KBytes")
    logger.log("--------------------------------------------")
    logger.log("")

    # Create sets
    cache = Cache(num_sets = num_sets, blocks_per_set = associativity, replacement_policy = replacement_policy,
                  address_bits = address_bits)

    # Initialize a class used to track various stats useful for debugging
    sim_metrics = SimulationMetrics(address_bits = address_bits)

    # Run the trace file
    with open(file = trace_file, mode = "r", encoding = "utf-8") as opened_trace:
        lines = opened_trace.readlines()
        line_num = 0
        for line in lines:
            # Skip comments or blank lines
            if "#" in line or line == "\n":
                continue

            # Print a status update every 50,000 lines
            line_num += 1
            if line_num % 50000 == 0:
                print(
                    f"Finished:{((line_num / len(lines)) * 100): .2f}%")

            # Parse address and send it to the simulation
            line = line.replace("\n", "")
            line = int(line)
            cache.load_block(address = line)
            sim_metrics.store_access(address = line)

    print()
    # Print the simulation stats
    logger.log("------------- SIMULATION STATS -------------")
    logger.log_and_print(f"Cache_Size: {cache_size} KBytes")
    logger.log_and_print(f"Block_Size: {block_size} words ({block_size_bytes} bytes)")
    logger.log_and_print(f"Associativity: {associativity} way")

    # Print out the correct replacement policy
    replacement_policy_string: str
    if replacement_policy == 1:
        replacement_policy_string = "LRU (least recently used)"
    elif replacement_policy == 2:
        replacement_policy_string = "Random"
    else:
        replacement_policy_string = "NMRU + Random (pseudo-LRU)"

    logger.log_and_print(f"Replacement_Policy: {replacement_policy_string}")

    cache.print_status(logger = logger)
    logger.log("--------------------------------------------")

    # Print the rest of the tracked stats (interesting, but not required except for debugging)
    logger.log("")
    max_blocks_in_set = 0
    set: CacheSet
    for set in cache.sets:
        if len(set.blocks) > max_blocks_in_set:
            max_blocks_in_set = len(set.blocks)
    logger.log(f"Max number of blocks in one set: {max_blocks_in_set}")

    max_accesses_for_tag = 0
    min_accesses_for_tag = 15000000000
    for tag_index_combined in sim_metrics.index_tag_accesses_dict:
        num_accesses = sim_metrics.index_tag_accesses_dict[tag_index_combined]
        max_accesses_for_tag = max(max_accesses_for_tag, num_accesses)
        min_accesses_for_tag = min(min_accesses_for_tag, num_accesses)

    logger.log(f"Max accesses for single index/tag: {max_accesses_for_tag}")
    logger.log(f"Min accesses for single index/tag: {min_accesses_for_tag}")
    logger.log(
        f"Total cache replacements: {cache.cache_replacements} / {cache.num_accesses} ({cache.cache_replacements / cache.num_accesses})")

    logger.log("")
    logger.log(f"Unique addresses in {trace_file.name}: {len(sim_metrics.unique_addresses)}")
    logger.log(f"Unique indices accessed: {len(sim_metrics.unique_indices)} / {num_sets}")
    logger.log(f"Unique index/tags accessed: {len(sim_metrics.unique_index_tags)}")

    print("\nMore detailed output file written to ./logs/ directory!")
