from pathlib import Path

if __name__ == "__main__":
    output_file = Path("configs_to_try.txt")
    output_file.touch(exist_ok = True)
    output_file.write_text("")

    with open(file = output_file, encoding = "utf-8", mode = "a") as opened:
        comment_line = "# Associativity | Replacement policy | Cache size (kb) | Block size (words)"
        opened.write(comment_line + "\n")

        # Associativity
        for associativity in [1, 2, 4, 8, 16]:
            for replacement_policy in [1, 2, 3]:
                for cache_size in [1, 2, 4, 8, 16, 32, 64, 128, 256]:
                    for block_size in [1, 2, 3, 4, 5, 6, 7, 8]:
                        opened.write(f"{associativity} {replacement_policy} {cache_size} {block_size}\n")
