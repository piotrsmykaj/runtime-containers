import argparse
import os
import re
from shutil import copy2, copytree, rmtree
import subprocess
import sys
import yaml


variables = {}

flavours = {
    'deb': 'debian:jessie'
}

parser = argparse.ArgumentParser(description='Runtime containers generator')
parser.add_argument('cmd', nargs='?', type=str, help='Command')
parser.add_argument('runtime', nargs='?', type=str, help='Runtime')
parser.add_argument('--version', nargs='*', default='all',
                    type=str, help='List of versions to compile')
parser.add_argument('--clean', dest='clean',
                    action='store_const', const=True, default=False)
args = parser.parse_args()

with open(args.runtime+'.yml', 'r') as data_template:
    template = yaml.load(data_template, Loader=yaml.Loader)

versions = list(filter(lambda x: args.version ==
                       'all' or x in args.version, template['versions']))


def leaf(path):
    """ Return leaf of given path """
    return path.split('/')[-1]


def parent(path):
    """ Return parent of given path """
    return '/'.join(path.split('/')[:-1])


def exec(cmd):
    """ Execute shell command """
    subprocess.call(cmd.split(' '))


def prepare_building_environment():
    """ Preparing files, dockerfiles and BATS tests """

    def get_component_path(component_name):
        return '/'.join([parent(os.path.realpath(__file__)), '../components', component_name, component_name+'.dtc'])

    def init_directories():
        if not os.path.exists('files'):
            os.mkdir('files')
        if not os.path.exists('dockerfiles'):
            os.mkdir('dockerfiles')

    def move_additional_files():
        for component in template['components']:
            component_path = get_component_path(component)
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

    def generate_dockerfile(version):
        with open('dockerfiles/{}_{}.d'.format(args.runtime, version), 'w') as dockerfile:
            # here replace by flavour image or version "example php:version"
            if version == 'generic':
                base = 'debian:jessie'
            else:
                base = '{}:{}'.format(args.runtime, version)
            dockerfile.write('FROM '+base+'\n')
            for component in template['components']:
                component_path = get_component_path(component)
                dockerfile.write(
                    open(component_path, 'r').read()+'\n')

    def generate_bats_file(version):
        with open('dockerfiles/{}_{}.bats'.format(args.runtime, version), 'w') as batsfile:
            batsfile.write('#!/usr/bin/env bats\n')
            for component in template['components']:
                component_path = parent(get_component_path(component))
                bats_path = '/'.join([component_path, 'tests',
                                      leaf(component_path)+'.bats'])
                with open(bats_path, 'r') as batscontent:
                    batsfile.write(batscontent.read() + '\n')

    def generate_bats_dockerfile(version):
        with open('dockerfiles/{}_{}.bats.d'.format(args.runtime, version), 'w') as batsdockerfile:
            # There you must specify the resulting tag
            batsdockerfile.write(
                'FROM '+'continuous:{}_{}'.format(args.runtime, version)+'\n')
            with open(parent(os.path.realpath(__file__))+'/../bats/batsimage.d', 'r') as batsdockerfilepart:
                batsdockerfile.write(batsdockerfilepart.read()+'\n')

    init_directories()
    move_additional_files()
    for version in versions:
        generate_dockerfile(version)
        generate_bats_dockerfile(version)
        generate_bats_file(version)


def generate_runtime_container():
    exec('echo \"Generating runtime containers...\"')
    for version in versions:
        print('docker build -f ./dockerfiles/{}_{}.d -t {} .'.format(
            args.runtime, version, 'continuous:{}_{}'.format(args.runtime, version)))
        exec('docker build -f ./dockerfiles/{}_{}.d -t {} .'.format(
            args.runtime, version, 'continuous:{}_{}'.format(args.runtime, version)))


def run_bats_container():
    exec('echo \"Generating bats container...\"')
    for version in versions:
        print('Preparing bats container for version : '+version)
        exec(
            'docker build -f ./dockerfiles/{}_{}.bats.d -t bats_tests .'.format(args.runtime, version))
        try:
            exec('docker run -it -v {}/dockerfiles/{}_{}.bats:/test.bats bats_tests'.format(
                os.getcwd(), args.runtime, version))
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
    if args.cmd == 'build':
        clean_directories()
        print('Building docker images : ')
        print('\n- '.join([' '] + versions))
        prepare_building_environment()
        generate_runtime_container()
        run_bats_container()
        if args.clean:
            clean_directories()
