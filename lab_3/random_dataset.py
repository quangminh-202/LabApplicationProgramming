import os
import random
import shutil
from annotation import Annotation

def dataset_random(path: str, path_random: str, ann: Annotation) -> None:
    if not os.path.isdir(path_random):
        try:
            os.mkdir(path_random)
        except OSError as err:
            print(f"Create director {path_random} failed")
            raise err

    folders = os.listdir(path)
    for folder in folders:
        files = os.listdir(os.path.join(path, folder))
        for file in files:
            shutil.copy(os.path.join(path, folder, file), path_random)
            file_random = f"{random.randint(0, 10000)}.text"
            while os.path.exists(os.path.join(path_random, file_random)):
                file_random = f"{random.randint(0, 10000)}.text"
            os.rename(os.path.join(path_random, file), os.path.join(path_random, file_random))
            ann.add_line(path_random, file_random, folder)


if __name__ == "__main__":
    path_dataset = "C:/Users/DELL/PycharmProjects/LabApplicationProgramming/lab_1/dataset"
    path_task = "C:/Users/DELL/PycharmProjects/LabApplicationProgramming/python/data_random"
    a = Annotation("file_csv_random.csv")
    dataset_random(path_dataset, path_task, a)