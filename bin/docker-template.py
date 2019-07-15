import argparse
import os
import re
from shutil import copy2, copytree, rmtree
import subprocess
import sys
import yaml

_ROOT = '/'.join([os.path.dirname(os.path.realpath(__file__)), '..'])
_BATSIMAGE = '/'.join([_ROOT,
                       'bats', 'batsimage.d'])
_TMP = '/'.join([_ROOT, 'bin', 'tmp'])
_FILES = '/'.join([_ROOT, 'bin', 'tmp', 'files'])
_DOCKERFILES = '/'.join([_ROOT, 'bin',
                         'tmp', 'dockerfiles'])
_COMPONENTS = '/'.join([_ROOT, 'components'])


def exec(cmd):
    """ Execute shell command """
    subprocess.call(cmd.split(' '))


def build(runtime, clean=False):
    """ Preparing files, dockerfiles and BATS tests """

    with open('/'.join([_ROOT, 'runtimes', runtime+'.yml']), 'r') as data_template:
        template = yaml.load(data_template, Loader=yaml.Loader)
        versions = list(filter(lambda x: args.version ==
                               'all' or x in args.version, template['versions']))

    def init_directories():
        try:
            rmtree(_TMP)
        except Exception as e:
            print('No need to clean tmp directory : ' + str(e))

        os.mkdir(_TMP)
        os.mkdir(_FILES)
        os.mkdir(_DOCKERFILES)

    def move_additional_files():
        for component in template['components']:
            src = '/'.join([_COMPONENTS, component, 'files'])
            if os.path.exists(src):
                dst = '/'.join([_FILES, component])
                os.mkdir(dst)
                for item in os.listdir(src):
                    obj = os.path.join(src, item)
                    res = os.path.join(dst, item)
                    if os.path.isdir(obj):
                        copytree(obj, res)
                    else:
                        copy2(obj, res)

    def generate_runtime_dockerfile(version):
        with open(_DOCKERFILES+'/{}_{}.d'.format(runtime, version), 'w') as dockerfile:
            # Here replace by flavour image or version "example php:version"
            if version == 'generic':
                base = 'debian:jessie'
            else:
                base = '{}:{}'.format(template['image'], version)
            dockerfile.write('FROM '+base+'\n')
            for component in template['components']:
                component_file = '/'.join([_COMPONENTS,
                                           component, template['flavour'], component+'.dtc'])
                dockerfile.write(
                    open(component_file, 'r').read()+'\n')

    def generate_bats_dockerfile(version):
        with open(_DOCKERFILES+'/{}_{}.bats.d'.format(runtime, version), 'w') as batsdockerfile:
            # There you must specify the resulting tag
            batsdockerfile.write(
                'FROM '+'continuous:{}_{}'.format(runtime, version)+'\n')
            with open(_BATSIMAGE, 'r') as batsdockerfilepart:
                batsdockerfile.write(batsdockerfilepart.read()+'\n')

    def generate_bats_file(version):
        with open(_DOCKERFILES+'/{}_{}.bats'.format(runtime, version), 'w') as batsfile:
            batsfile.write('#!/usr/bin/env bats\n')
            for component in template['components']:
                bats_path = '/'.join([_COMPONENTS, component, 'tests',
                                      component+'.bats'])
                with open(bats_path, 'r') as batscontent:
                    batsfile.write(batscontent.read() + '\n')

    def generate_runtime_container(version):
        print('docker build -f {}/dockerfiles/{}_{}.d -t {} {}'.format(
            _TMP, runtime, version, 'continuous:{}_{}'.format(runtime, version), _TMP))
        exec('docker build -f {}/dockerfiles/{}_{}.d -t {} {}'.format(
            _TMP, runtime, version, 'continuous:{}_{}'.format(runtime, version), _TMP))

    def generate_and_run_bats_container(version):
        print('Preparing bats container for version : '+version)
        exec(
            'docker build -f {}/dockerfiles/{}_{}.bats.d -t bats_tests {}'.format(_TMP, runtime, version, _TMP))
        try:
            exec('docker run -it -v {}/dockerfiles/{}_{}.bats:/test.bats bats_tests'.format(
                _TMP, runtime, version))
        except Exception as e:
            print('One or more bats tests failed')
        exec('docker image rm -f bats_tests')

    def clean_directories():
        rmtree(_TMP)

    print('Building docker images : ')
    print('\n- '.join([' '] + versions))

    init_directories()
    move_additional_files()
    for version in versions:
        generate_runtime_dockerfile(version)
        generate_runtime_container(version)
        generate_bats_dockerfile(version)
        generate_bats_file(version)
        generate_and_run_bats_container(version)
    if clean:
        clean_directories()


if __name__ == '__main__':
    variables = {}

    flavours = {
        'deb': 'debian:jessie'
    }

    parser = argparse.ArgumentParser(
        description='Runtime containers generator')
    parser.add_argument('cmd', nargs='?', type=str, help='Command')
    parser.add_argument('runtime', nargs='?', type=str, help='Runtime')
    parser.add_argument('--version', nargs='*', default='all',
                        type=str, help='List of versions to compile')
    parser.add_argument('--clean', dest='clean',
                        action='store_const', const=True, default=False)
    args = parser.parse_args()

    if args.cmd == 'build':
        build(args.runtime, args.clean)
