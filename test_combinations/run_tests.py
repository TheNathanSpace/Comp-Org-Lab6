from pathlib import Path

import linuxized

if __name__ == "__main__":
    output = Path("tested_output.txt")
    output.touch(exist_ok = True)
    output.write_text("")

    to_try = Path("configs_to_try.txt")
    lines = None
    with open(file = to_try, encoding = "utf8", mode = "r") as opened:
        lines = opened.readlines()

    line_num = 0
    for line in lines:
        if "#" in line:
            continue
        line_num += 1
        if line_num % 10 == 0:
            print(f"On line {line_num}/{len(lines)} ({(line_num / len(lines)): .2f})")

        line = line.replace("\n", "")
        line_split = line.split(" ")
        linuxized.run_test(int(line_split[0]), int(line_split[1]), int(line_split[2]), int(line_split[3]))
