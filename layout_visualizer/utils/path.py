import os


def get_src_dir() -> str:
    return os.path.dirname(os.path.dirname(__file__))
