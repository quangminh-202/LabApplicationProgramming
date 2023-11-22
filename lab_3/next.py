import os
import re #regular expression


def next_file(path: str):
    """
    1.Проверьте, существует ли файл. Если он не существует, он выдает исключение FileExistsError.
    2.Отделите имя файла и родительскую папку от пути.
    3.Найдите и извлеките строки чисел из имени файла filename.
    4.Увеличьте числовое значение до 1 и отформатируйте новое число так, чтобы оно содержало не менее 4 цифр.
    5.Замените старую числовую строку новым номером в имени файла.
    6.Объедините родительскую папку и новое имя файла, чтобы создать полный путь к новому файлу.
    7.Проверьте, существует ли новый файл. Если новый файл существует, он возвращает путь к новому файлу;
    в противном случае возвращает None.
    """
    if not os.path.exists(path):
        raise FileExistsError(f'The {path} file does not exist.')
    direct, filename = os.path.split(path) #tach ten tep
    a = "".join(re.findall(r'\d', filename))
    number = int(a) + 1
    file_new = re.sub(a, f'{number:04d}', filename)
    file_new = os.path.join(direct, file_new)
    if os.path.exists(file_new):
        return file_new
    else:
        return None

if __name__ == "__main__":
    path = "C:/Users/DELL/PycharmProjects/LabApplicationProgramming/python/dataset_copy"
    file_path = os.path.join(path, '1_0150.txt')
    file_path = next_file(file_path)
    print(file_path)