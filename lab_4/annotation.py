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
                writer.writerow(["Absolute Path", "Relative Path", "Label"])
                self.rows += 1
            absolute_path = os.path.join(path, filename).replace("\\", "/")
            writer.writerow([absolute_path, os.path.relpath(os.path.join(path, filename)), label])
            self.rows += 1