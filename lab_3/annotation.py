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
        res = []  # Danh sách kết quả
        try:
            with open(self.filename, 'r') as file:
                rows = csv.DictReader(file)
                for row in rows:
                    if row.get(self.__header[2]) == label:
                        res.append(row.get(self.__header[0]))
            if not res:
                logging.warning(f"Không tìm thấy đường dẫn cho nhãn {label} trong {self.filename}.")
        except FileNotFoundError:
            logging.warning(f"Tệp tin {self.filename} không tồn tại.")
        except OSError as err:
            logging.warning(f'Khi mở tệp tin {self.filename} xảy ra lỗi:\n{err}.')
        return res
