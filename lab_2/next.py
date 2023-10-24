import os
import re #regular expression


def next_file(path: str):
    if not os.path.exists(path):
        raise FileExistsError(f'The {path} file does not exist.')
    direct, filename = os.path.split(path)
    a = "".join(re.findall(r'\d', filename))
    number = int(a) + 1
    file_new = re.sub(a, f'{number:04d}', filename)
    file_new = os.path.join(direct, file_new)
    if os.path.exists(file_new):
        return file_new
    else:
        return None