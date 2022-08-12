import os


def create_dir_if_not_exist(directory: str) -> str:
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory
