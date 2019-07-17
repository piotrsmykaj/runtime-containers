#!/usr/local/bin/python3

import argparse
import os
import re
from shutil import copy2, copytree, rmtree
import subprocess
import sys
import yaml


class App:

    def __init__(self, args):

        self.root = '/'.join([os.path.dirname(os.path.realpath(__file__)), '..'])
        self.batsimage = '/'.join([self.root, 'bats', 'batsimage.d'])
        self.logs = '/'.join([self.root, 'bin', 'logs.txt'])
        self.tmp = '/'.join([self.root, 'bin', 'tmp'])
        self.files = '/'.join([self.root, 'bin', 'tmp', 'files'])
        self.dockerfiles = '/'.join([self.root, 'bin', 'tmp', 'dockerfiles'])
        self.components = '/'.join([self.root, 'components'])
        self.runtime = args.runtime
        self.cmd = args.cmd
        self.clean = args.clean
        self.verbose = args.verbose
        self.replace = args.replace
        with open('/'.join([self.root, 'runtimes', self.runtime+'.yml']), 'r') as data_template:
            self.template = yaml.load(data_template, Loader=yaml.Loader)
            self.versions = list(filter(lambda x: args.version ==
                                        'all' or x in args.version, self.template['versions']))
        self.running_map = {
            "build": self.build,
            "test": self.test
        }
        self.color_map = {
            "blue": "\033[1;34;40m",
            "red": "\O33[1;31;40m",
            "green": "\033[1;32;40m",
            "yellow": "\033[1;33;40m",
            "normal": "\033[0m"
        }

    def display(self, text, color):
        if color not in self.color_map:
            raise Exception('The following color is not handled : '+color)
        print(self.color_map[color],
              text,
              self.color_map["normal"])

    def exec(self, cmd, print_output=True):
        """ Execute shell command """
        if print_output:
            """ Store outputs in logsfile """
            with open(self.logs, 'a+') as outputfile:
                output = subprocess.run(
                    cmd.split(' '), stdout=outputfile)
        else:
            """ Display outputs into the shell """
            output = subprocess.run(cmd.split(' '), capture_output=False)
        return output.returncode

    def clean_up_context(self):
        if os.path.exists(self.tmp):
            self.exec('rm -rf {}'.format(self.tmp), not self.verbose)
        if os.path.exists(self.logs):
            self.exec('rm -rf {}'.format(self.logs), not self.verbose)

    def init_directories(self):
        self.clean_up_context()
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
            self.display('docker build -f {}/dockerfiles/{}_{}.d -t {} {}'.format(
                self.tmp, self.runtime, version, 'continuous:{}_{}'.format(self.runtime, version), self.tmp), "yellow")
            self.exec('docker build -f {}/dockerfiles/{}_{}.d -t {} {}'.format(
                self.tmp, self.runtime, version, 'continuous:{}_{}'.format(self.runtime, version), self.tmp), not self.verbose)

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
                    bats_path = '/'.join([self.components, component, self.template['flavour'], 'tests',
                                          component+'.bats'])
                    with open(bats_path, 'r') as batscontent:
                        batsfile.write(batscontent.read() + '\n')

    def generate_and_run_bats_container(self):
        for version in self.versions:
            self.display(
                'Preparing bats container for version : '+version, "yellow")
            self.exec(
                'docker build -f {}/dockerfiles/{}_{}.bats.d -t bats_tests {}'.format(self.tmp, self.runtime, version, self.tmp), not self.verbose)
            try:
                self.display(
                    "Results of bats tests for version : "+version, "green")
                self.exec('docker run -it -v {}/dockerfiles/{}_{}.bats:/test.bats bats_tests'.format(
                    self.tmp, self.runtime, version), False)
            except Exception as e:
                self.display('One or more bats tests failed', "red")
            self.exec('docker image rm -f bats_tests', not self.verbose)

    def build(self):
        """ Preparing files, dockerfiles and BATS tests """

        if not self.replace:
            self.versions = list(filter(lambda version:
                                        self.exec('/'.join([self.root, 'bin', 'check_container.sh continuous:{}_{}'
                                                            .format(self.runtime, version)]), not self.verbose) != 0, self.versions))
        self.display('Building docker images : \n', 'blue')
        self.display('\n'.join(self.versions), 'blue')

        self.init_directories()
        self.move_additional_files()
        self.generate_runtime_dockerfile()
        self.generate_runtime_container()
        self.generate_bats_dockerfile()
        self.generate_bats_file()
        self.generate_and_run_bats_container()

        self.versions = list(filter(lambda version:
                                    self.exec('/'.join([self.root, 'bin', 'check_container.sh continuous:{}_{}'
                                                        .format(self.runtime, version)]), not self.verbose) == 0, self.versions))

        self.display('Versions that have been created : \n' +
                     '\n'.join(self.versions), "green")

    def test(self):
        self.display(' ------ Testing docker images ------ ', "normal")

        # For each version tests if the associated container exists

        self.display('Versions that are supposed to exist : \n' +
                     '\n'.join(self.versions), "blue")
        self.versions = list(filter(lambda version:
                                    self.exec('/'.join([self.root, 'bin', 'check_container.sh continuous:{}_{}'
                                                        .format(self.runtime, version)]), not self.verbose) == 0, self.versions))
        self.display('Versions that really exist : \n' +
                     '\n'.join(self.versions), "blue")

        self.init_directories()
        self.move_additional_files()
        self.generate_bats_dockerfile()
        self.generate_bats_file()
        self.generate_and_run_bats_container()

    def run(self):
        if self.cmd in self.running_map:
            self.running_map[self.cmd]()
            if self.clean:
                self.clean_up_context()
        else:
            raise Exception(
                'The following command is not handled : ' + self.cmd)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Continuous runtime container generator')
    parser.add_argument('cmd', nargs='?', type=str, help='Command')
    parser.add_argument('runtime', nargs='?', type=str, help='Runtime')
    parser.add_argument('--version', nargs='*', default='all',
                        type=str, help='List of versions to compile')
    parser.add_argument('--clean', dest='clean', help='Remove all temporary files',
                        action='store_const', const=True, default=False)
    parser.add_argument('--verbose', dest='verbose', help='Print the entire output',
                        action='store_const', const=True, default=False)
    parser.add_argument('--replace', dest='replace', help='Rebuild existing images',
                        action='store_const', const=True, default=False)
    args = parser.parse_args()
    context = App(args)
    context.run()
