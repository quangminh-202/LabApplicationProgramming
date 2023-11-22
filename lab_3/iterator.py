import os

class AnnIterator:
    def __init__(self, directory: str):
        self.directory = directory
        self.files = os.listdir(directory)
        self.current_index = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index < len(self.files):
            next_file = self.files[self.current_index]
            self.current_index += 1
            return next_file
        else:
            raise StopIteration

if __name__ == "__main__":
    path = "C:/Users/DELL/PycharmProjects/LabApplicationProgramming/python/dataset_copy"
    it = AnnIterator(path)
    print(it.__next__())
    print(it.__next__())
    print(it.__next__())