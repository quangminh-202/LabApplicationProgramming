from annotation import Annotation
import os
import shutil
#shutil sao chép và thay đổi tên tệp


def copy_dataset(path: str, path_copy: str, ann: Annotation) -> None:
    if not os.path.isdir(path_copy):
        try:
            os.mkdir(path_copy)
        except OSError as err:
            print(f"Create director {path_copy} failed")
            raise err
    folders = os.listdir(path)
    for folder in folders:
        files = os.listdir(os.path.join(path, folder))
        for file in files:
            shutil.copy(os.path.join(path, folder, file), path_copy)
            os.rename(os.path.join(path_copy, file), os.path.join(path_copy, f"{folder}_{file}"))
            ann.add_line(path_copy, f"{folder}_{file}", folder)


if __name__ == "__main__":
    path_copy = "C:/Users/DELL/PycharmProjects/LabApplicationProgramming/python/dataset_copy"
    path = "C:/Users/DELL/PycharmProjects/LabApplicationProgramming/lab_1/dataset"
    a = Annotation("file_csv_copy.csv")
    copy_dataset(path, path_copy, a)