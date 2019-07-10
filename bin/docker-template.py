import os
import re
import sys
import subprocess
import xml.etree.ElementTree as et
from shutil import copy2, copytree, rmtree


variables = {}


def leaf(path):
    """ Return leaf of given path """
    return path.split('/')[-1]


def parent(path):
    """ Return parent of given path """
    return '/'.join(path.split('/')[:-1])


def exec(cmd):
    """ Execute shell command """
    subprocess.call(cmd.split(' '))


def get_inputs():
    """ Store inputs in a dictionary """
    for i in range(1, len(sys.argv)):
        query = re.search('--(\w+)=([a-zA-Z0-9_\.\-\:]+)', sys.argv[i])
        try:
            variables[query.group(1)] = query.group(2)
        except Exception as e:
            print('Error while getting arguments : ' + str(e))


def prepare_environment():
    """ Preparing files, dockerfiles and BATS tests """
    def init_directories():
        if not os.path.exists('files'):
            os.mkdir('files')
        if not os.path.exists('dockerfiles'):
            os.mkdir('dockerfiles')

    def generate_dockerfile():
        with open('dockerfiles/'+variables['template']+'.d', 'w') as dockerfile:
            dockerfile.write('FROM '+variables['base']+'\n')
            root = et.parse('generic.xml').getroot()
            for component in root.iter('component'):
                dockerfile.write(
                    open(component.attrib['path'], 'r').read()+'\n')

    def move_additional_files():
        root = et.parse('generic.xml').getroot()
        for component in root.iter('component'):
            component_path = component.attrib['path']
            src = parent(component_path)+'/files'
            if os.path.exists(src):
                dst = 'files/' + leaf(parent(component_path))
                os.mkdir(dst)
                for item in os.listdir(src):
                    obj = os.path.join(src, item)
                    res = os.path.join(dst, item)
                    if os.path.isdir(obj):
                        copytree(obj, res)
                    else:
                        copy2(obj, res)

    def generate_bats_file():
        with open('dockerfiles/'+variables['template']+'.bats', 'w') as batsfile:
            batsfile.write('#!/usr/bin/env bats\n')
            root = et.parse('generic.xml').getroot()
            for component in root.iter('component'):
                component_path = parent(component.attrib['path'])
                bats_path = '/'.join([component_path, 'tests',
                                      leaf(component_path)+'.bats'])
                with open(bats_path, 'r') as batscontent:
                    batsfile.write(batscontent.read() + '\n')

    def generate_bats_dockerfile():
        with open('dockerfiles/'+variables['template']+'.bats.d', 'w') as batsdockerfile:
            batsdockerfile.write('FROM '+variables['tag']+'\n')
            root = et.parse('generic.xml').getroot()
            for item in root.iter('bats'):
                with open(item.attrib['path'], 'r') as batsdockerfilepart:
                    batsdockerfile.write(batsdockerfilepart.read()+'\n')

    init_directories()
    generate_dockerfile()
    move_additional_files()
    generate_bats_file()
    generate_bats_dockerfile()


def generate_runtime_container():
    exec('echo \"Generating runtime container...\"')
    exec('docker build -f ./dockerfiles/{}.d -t {} .'.format(
        variables['template'], variables['tag']))


def run_bats_container():
    exec('echo \"Generating bats container...\"')
    exec(
        'docker build -f ./dockerfiles/{}.bats.d -t bats_tests .'.format(variables['template']))
    try:
        exec('docker run -it -v {}/dockerfiles/{}.bats:/test.bats bats_tests'.format(
            os.getcwd(), variables['template']))
    except Exception as e:
        print('One or more bats tests failed')
    exec('docker image rm -f bats_tests')


def clean_directories():
    try:
        rmtree('files')
    except Exception as e:
        print('Error while deleting \"files\"')
    try:
        rmtree('dockerfiles')
    except Exception as e:
        print('Error while deleting \"dockerfiles\"')


if __name__ == '__main__':
    get_inputs()
    prepare_environment()
    generate_runtime_container()
    run_bats_container()
    clean_directories()
