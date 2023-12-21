import os
import csv


class Annotation:
    def __init__(self, filename: str):
        self.rows = 0
        self.filename = filename

    def add_line(self, path: str, filename: str, label: str) -> None:
        with open(self.filename, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            if self.rows == 0:
                writer.writerow(["count", "num", "text"])
                self.rows += 1
            path_data =   os.path.join(path, filename)
            with open(path_data, "r", encoding="utf-8") as file:
                content = file.read()
            writer.writerow([self.rows, label, content])
            self.rows += 1