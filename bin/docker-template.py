#!/usr/local/bin/python3

import argparse
import os
import re
from shutil import copy2, copytree, rmtree
import subprocess
import sys
import yaml


_ROOT = '/'.join([os.path.dirname(os.path.realpath(__file__)), '..'])
_BATSIMAGE = '/'.join([_ROOT, 'bats', 'batsimage.d'])
_TMP = '/'.join([_ROOT, 'bin', 'tmp'])
_FILES = '/'.join([_ROOT, 'bin', 'tmp', 'files'])
_DOCKERFILES = '/'.join([_ROOT, 'bin', 'tmp', 'dockerfiles'])
_COMPONENTS = '/'.join([_ROOT, 'components'])


class App:

    def __init__(self, args):

        self.root = '/'.join([os.path.dirname(os.path.realpath(__file__)), '..'])
        self.batsimage = '/'.join([self.root, 'bats', 'batsimage.d'])
        self.tmp = '/'.join([self.root, 'bin', 'tmp'])
        self.files = '/'.join([self.root, 'bin', 'tmp', 'files'])
        self.dockerfiles = '/'.join([self.root, 'bin', 'tmp', 'dockerfiles'])
        self.components = '/'.join([self.root, 'components'])
        self.runtime = args.runtime
        self.cmd = args.cmd
        self.clean = args.clean
        with open('/'.join([self.root, 'runtimes', self.runtime+'.yml']), 'r') as data_template:
            self.template = yaml.load(data_template, Loader=yaml.Loader)
            self.versions = list(filter(lambda x: args.version ==
                                        'all' or x in args.version, self.template['versions']))
        self.running_map = {
            "build": self.build,
            "test": self.test
        }

    def exec(self, cmd, print_output=True):
        """ Execute shell command """
        return subprocess.run(cmd.split(' '), capture_output=print_output).returncode

    def init_directories(self):
        self.exec('rm -rf '+self.tmp)
        os.mkdir(self.tmp)
        os.mkdir(self.files)
        os.mkdir(self.dockerfiles)

    def move_additional_files(self):
        for component in self.template['components']:
            src = '/'.join([self.components, component, 'files'])
            if os.path.exists(src):
                dst = '/'.join([self.files, component])
                os.mkdir(dst)
                for item in os.listdir(src):
                    obj = os.path.join(src, item)
                    res = os.path.join(dst, item)
                    if os.path.isdir(obj):
                        copytree(obj, res)
                    else:
                        copy2(obj, res)

    def generate_runtime_dockerfile(self):
        for version in self.versions:
            with open(self.dockerfiles+'/{}_{}.d'.format(self.runtime, version), 'w') as dockerfile:
                # Here replace by flavour image or version "example php:version"
                if version == 'generic':
                    base = 'debian:jessie'
                else:
                    base = '{}:{}'.format(self.template['image'], version)
                dockerfile.write('FROM '+base+'\n')
                for component in self.template['components']:
                    component_file = '/'.join([self.components,
                                               component, self.template['flavour'], component+'.dtc'])
                    dockerfile.write(
                        open(component_file, 'r').read()+'\n')

    def generate_runtime_container(self):
        for version in self.versions:
            print('docker build -f {}/dockerfiles/{}_{}.d -t {} {}'.format(
                self.tmp, self.runtime, version, 'continuous:{}_{}'.format(self.runtime, version), self.tmp))
            self.exec('docker build -f {}/dockerfiles/{}_{}.d -t {} {}'.format(
                self.tmp, self.runtime, version, 'continuous:{}_{}'.format(self.runtime, version), self.tmp))

    def generate_bats_dockerfile(self):
        for version in self.versions:
            with open(self.dockerfiles+'/{}_{}.bats.d'.format(self.runtime, version), 'w') as batsdockerfile:
                # There you must specify the resulting tag
                batsdockerfile.write(
                    'FROM '+'continuous:{}_{}'.format(self.runtime, version)+'\n')
                with open(self.batsimage, 'r') as batsdockerfilepart:
                    batsdockerfile.write(batsdockerfilepart.read()+'\n')

    def generate_bats_file(self):
        for version in self.versions:
            with open(self.dockerfiles+'/{}_{}.bats'.format(self.runtime, version), 'w') as batsfile:
                batsfile.write('#!/usr/bin/env bats\n')
                for component in self.template['components']:
                    bats_path = '/'.join([self.components, component, 'tests',
                                          component+'.bats'])
                    with open(bats_path, 'r') as batscontent:
                        batsfile.write(batscontent.read() + '\n')

    def generate_and_run_bats_container(self):
        for version in self.versions:
            print('Preparing bats container for version : '+version)
            self.exec(
                'docker build -f {}/dockerfiles/{}_{}.bats.d -t bats_tests {}'.format(self.tmp, self.runtime, version, self.tmp))
            try:
                print(
                    "Results of bats tests for version : "+version)
                self.exec('docker run -it -v {}/dockerfiles/{}_{}.bats:/test.bats bats_tests'.format(
                    self.tmp, self.runtime, version), False)
            except Exception as e:
                print('One or more bats tests failed')
            self.exec('docker image rm -f bats_tests')

    def clean_directories(self):
        rmtree(self.tmp)

    def build(self):
        """ Preparing files, dockerfiles and BATS tests """

        print('Building docker images : ')
        print('\n- '.join([' '] + self.versions))

        self.init_directories()
        self.move_additional_files()
        self.generate_runtime_dockerfile()
        self.generate_runtime_container()
        self.generate_bats_dockerfile()
        self.generate_bats_file()
        self.generate_and_run_bats_container()

    def test(self):
        print(' ------ Testing docker images ------ ')

        # For each version tests if the associated container exists

        print('Versions that are supposed to exist : \n' +
              '\n'.join(self.versions))
        self.versions = list(filter(lambda version:
                                    self.exec('/'.join([self.root, 'bin', 'check_container.sh continuous:{}_{}'
                                                        .format(self.runtime, version)])) == 0, self.versions))
        print('Versions that really exist : \n' + '\n'.join(self.versions))

        self.init_directories()
        self.move_additional_files()
        self.generate_bats_dockerfile()
        self.generate_bats_file()
        self.generate_and_run_bats_container()

    def run(self):
        if self.cmd in self.running_map:
            self.running_map[self.cmd]()
            if self.clean:
                self.clean_directories()
        else:
            raise Exception('Command is not handled')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Runtime containers generator')
    parser.add_argument('cmd', nargs='?', type=str, help='Command')
    parser.add_argument('runtime', nargs='?', type=str, help='Runtime')
    parser.add_argument('--version', nargs='*', default='all',
                        type=str, help='List of versions to compile')
    parser.add_argument('--clean', dest='clean',
                        action='store_const', const=True, default=False)
    args = parser.parse_args()
    context = App(args)
    context.run()
