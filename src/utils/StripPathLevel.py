import os.path
import configparser
import io

def strip_path_level(path, level = 0):
    head = path
    for i in range(0, level):
        (head, tail) = os.path.split(head)
    return head