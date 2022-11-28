import datetime
from pathlib import Path


class Logger:
    def __init__(self):
        log_dir = Path.cwd() / Path("logs")
        log_dir.mkdir(exist_ok = True)

        self.log_file = Path.cwd() / Path(f"logs/log_{int(datetime.datetime.utcnow().timestamp())}.txt")
        self.log_file.touch(exist_ok = True)

    def log(self, string):
        string = str(string)
        with open(file = self.log_file, mode = "a") as opened:
            # {datetime.datetime.utcnow()}:
            opened.write(f"{string}\n")

    def log_and_print(self, string):
        string = str(string)
        print(string)
        self.log(string)
