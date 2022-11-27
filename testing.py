from pathlib import Path

if __name__ == '__main__':
    trace_file = Path("tracefile.txt")
    with open(trace_file, mode = "r") as opened:
        lines = opened.readlines()
        max = 0
        min = 9999999999999999999999
        for line in lines:
            if int(line) < min:
                min = int(line)
            if int(line) > max:
                max = int(line)

        print(f"Min: {min}")
        print(f"Max: {max}")