# Cache Simulator

For Computer Organization Lab 6.

## Installation/Usage

You just need Python 3; no additional packages must be installed. Define settings in `config.txt` and just run `src/main.py`.

Output is saved to the ./logs/ directory.

### Settings

Change settings in the file `config.txt`:

```
# The number of blocks per set in the associative cache (power of 2 from 0-16)
associativity=2

# The replacement policy
#  1. LRU (least recently used)
#  2. Random
#  3. NMRU + Random (pseudo-LRU)
replacement-policy=3

# Cache size in KB (max of 256KB)
cache-size=32

# Block size in words (max of 8 words)
block-size=4
```

The trace file used is hardcoded to `tracefile.txt`; change line 54 in `main.py` to use a different file. Comments/blank
lines are allowed (see `my_tracefile.txt`).