""" This function takes the maker configuration file ctl and overrides settings if found in the relevant section of config.json"""
import os.path
import configparser
import io

from string import Template

def read_file(filename):
    ''' Reads a file and returns its contents as a single string '''
    with open(filename) as contents:
        return ''.join(contents.readlines())

def read_yml(CONFIG, yml):
    config = Template(read_file(yml))
    return config.safe_substitute(seq_file=CONFIG["base"]["seq_file"], 
                           format=CONFIG["base"]["format"], 
                           cpus=CONFIG["base"]["cpus"], 
                           output=CONFIG["base"]["output"], 
                           rmlib=CONFIG["base"]["rmlib"], 
                           run_log=CONFIG["base"]["run_log"], 
                           cluster_log=CONFIG["base"]["cluster_log"])
    
    

def strip_path_level(path, level = 0):
    head = path
    for i in range(0, level):
        (head, tail) = os.path.split(head)
    return head
