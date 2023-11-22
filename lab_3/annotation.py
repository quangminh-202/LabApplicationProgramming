import os
import csv
import logging

class Annotation:
    def __init__(self, filename: str):
        self.rows = 0
        self.filename = filename
        self.__header = ['Absolute Path', 'Relative Path', 'Label']

    def add_line(self, path: str, filename: str, label: str) -> None:
        with open(self.filename, "a", encoding="utf-8", newline ="") as f:
            #a : append mode
            #CSV = Comma-Separated Values
            write = csv.writer(f, quoting=csv.QUOTE_ALL)
            if self.rows == 0:
                write.writerow(["Absolute Path", "Relative Path", "Label"])
                self.rows += 1
            write.writerow([os.path.join(path, filename), os.path.relpath(os.path.join(path, filename))], label)
            self.rows += 1

    def first_file_text(self, label: str):
        res = [] #list result
        try:
            with open(self.filename, 'r') as file:
                rows = csv.DictReader(file)
                for row in rows:
                    if row[self.__header[2]] == label:
                        return row[self.__header[0]]
        except OSError as err:
            logging.warning(f' При попытке открытия аннотации {self.filename} произошла ошибка:\n{err}.')
        return res[0]