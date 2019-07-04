import os
import re
import sys
from shutil import copy2

""" State :

php710 build succcesfully : make php710
But we still need to get a copy of all files in /files : this is not efficient
This script must copy each needed files.

"""


def get_variables():
    variables = {}
    for k in range(1, len(sys.argv)):
        parsing = re.search('--(\w+)=([a-zA-Z0-9_\.\-]+)', sys.argv[k])
        try:
            variables[parsing.group(1)] = parsing.group(2)
        except Exception as e:
            raise Exception('Error while getting arguments : ' + str(e))
    return variables


variables = get_variables()


def parent(path):
    """ Parent of path file or folder """
    return '/'.join(path.split('/')[:-1])


def transfer(file2add):
    """ Copy a file and if needed recursevily reconstructs the new path """
    def safe_path(path):
        if not os.path.exists(path):
            safe_path(parent(path))
            os.mkdir(path)
    original_file_path = os.path.dirname(
        os.path.realpath(__file__)) + '/../' + file2add.group(2)
    new_file_path = os.getcwd() + '/' + file2add.group(2)
    safe_path(parent(new_file_path))
    copy2(original_file_path, new_file_path)


def match_component(text):
    return re.search(';([a-zA-Z0-9_\.\-\/]+)', text)


def match_additional_files(text):
    return re.search('(ADD|COPY)+ ([a-zA-Z0-9_\.\-\/]+)', text)


def replace_component(line):
    def load_component(match_object):
        with open(match_object.group(1), 'r') as component:
            content = component.read()
            lines = content.split('\n')
            for line in lines:
                file2add = match_additional_files(line)
                if file2add is not None:
                    transfer(file2add)
            return content

    return re.sub(';([a-zA-Z0-9_\.\-\/]+\.dtc)', load_component, line)


def replace_variable(line):
    def load_variable(match_object):
        try:
            return variables[match_object.group(1)]
        except Exception as e:
            print('Error while getting variables : ' + str(e))
            return match_object.group(0)

    return re.sub('%(\w+)', load_variable, line)


if __name__ == '__main__':
    with open(variables['template'], 'r') as template:
        with open('Dockerfile', 'w') as output:
            output.write(replace_component(
                replace_variable(template.read())))
    output.close()
    template.close()
