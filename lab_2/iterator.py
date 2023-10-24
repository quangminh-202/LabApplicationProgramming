import os
from next import next_file


class AnnIterator:
    def __init__(self, path: str):
        self.path = path

    def __iter__(self):
        return self

    def __next__(self, direct: str):
        path_new = os.path.join(self.path, direct)
        return next_file(path_new)

if __name__ == "__main__":
    path = "C:/Users/DELL/PycharmProjects/LabApplicationProgramming/python/dataset_copy"
    it = AnnIterator(path)
    print(it.__next__('dog_0150.jpg'))
    print(it.__next__('dog_0151.jpg'))
    print(it.__next__('dog_0152.jpg'))