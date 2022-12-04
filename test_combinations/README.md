`configs_to_try.txt` is a file containing every associativity/replacement policy/cache size/block size combination.

`generate_tests.py` was used to generate the `configs_to_try.txt` file.

`linuxized.py` is a streamlined version of the cache simulator `main.py` that takes in config arguments and returns a hit rate (following the [Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy)). This depends on the modules in `../src`.

`run_tests.py` runs `linuxized.py` for each config combination in `configs_to_try.txt`. Results are written to `tested_output.py` (with the hit rate as the 5th value).

`sort_test_outputs.py` sorts the results in `tested_output.txt`, outputting two files:

 - `tested_output_sorted.txt` sorts all test results by hit rate.
 - `tested_output_sorted_sizes.txt` separates test results by cache size and sorts those subsets by hit rate.